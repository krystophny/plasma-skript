#!/usr/bin/env python3
"""Exercise playback, fallback, fullscreen and theme switching in a real browser."""
import argparse
import json
from pathlib import Path
import time
from playwright.sync_api import sync_playwright


def audit(browser, base, media, artifacts, device=None):
    context = browser.new_context(**(device or {'viewport': {'width': 1366, 'height': 1024}}), reduced_motion='reduce')
    # Play the exact newly rendered media while leaving all real HTML/JS intact.
    def stream(route):
        filename = route.request.url.split('/animations/')[-1].split('?')[0]
        slug = filename.removesuffix('.mp4').replace('_', '-')
        route.fulfill(path=str(media / (slug + '.mp4')), content_type='video/mp4')
    context.route('https://cloud.tugraz.at/**/animations/*.mp4*', stream)
    page = context.new_page()
    errors, downloads = [], []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('download', lambda item: downloads.append(item.suggested_filename))
    page.goto(base + '/chapters/04-plasma-oscillations.html')
    video = page.locator('video[src*="plasma_oscillation.mp4"]')
    player = video.locator('..')
    controls = player.locator('.animation-controls')
    assert video.evaluate('(v) => v.paused && !v.controls && v.muted && v.playsInline')
    assert player.locator('button').count() == 1, 'Only the small fullscreen button belongs in the toolbar'
    assert not player.locator('.animation-toggle, .animation-restart').count()
    video.click()
    page.wait_for_function('document.querySelector("video[src*=plasma_oscillation]").currentTime > 0.3')
    assert not page.evaluate('Boolean(document.fullscreenElement)')
    assert not player.evaluate('(p) => p.classList.contains("animation-full-window")'), 'A video click must remain inline'
    video.click()
    assert video.evaluate('(v) => v.paused')
    video.press('Home')
    assert video.evaluate('(v) => v.currentTime < 0.2 && v.paused')
    video.press('ArrowRight')
    assert video.evaluate('(v) => v.currentTime >= 4.9 && v.paused')
    video.press('ArrowLeft')
    assert video.evaluate('(v) => v.currentTime < 0.2')
    seek = player.get_by_role('slider', name='Animation position')
    seek.focus(); seek.press('End')
    assert video.evaluate('(v) => Math.abs(v.currentTime - v.duration) < 0.2')
    seek.press('Home')
    assert video.evaluate('(v) => v.currentTime < 0.2 && v.paused')
    video.focus()
    page.wait_for_timeout(950)
    assert controls.evaluate('(c) => Number(getComputedStyle(c).opacity)') == 0, 'Toolbar must fade in less than a second'
    player.screenshot(path=str(artifacts / 'inline-clean.png'))
    video.hover()
    bounds = video.bounding_box()
    page.mouse.move(bounds['x'] + bounds['width'] / 2 + 2, bounds['y'] + bounds['height'] / 2)
    assert controls.evaluate('(c) => Number.parseFloat(getComputedStyle(c).height)') <= 36
    player.screenshot(path=str(artifacts / 'inline-controls.png'))
    player.get_by_role('button', name='Full screen', exact=True).click()
    page.wait_for_timeout(300)
    full = page.evaluate('Boolean(document.fullscreenElement)')
    window = player.evaluate('(p) => p.classList.contains("animation-full-window")')
    assert full or window, 'Full-screen request neither succeeded nor opened the viewport fallback'
    assert video.evaluate('(v) => v.paused'), 'Fullscreen must preserve playback state'
    if full:
        page.screenshot(path=str(artifacts / 'fullscreen.png'))
        page.evaluate('document.exitFullscreen?.()')
    elif window:
        page.screenshot(path=str(artifacts / 'fullscreen-window.png'))
        video.hover()
        player.get_by_role('button', name='Exit full screen', exact=True).click()
    assert not errors, errors
    assert not downloads, downloads
    video.screenshot(path=str(artifacts / 'animation.png'))
    # The media src must remain unchanged when the reading theme changes.
    source = video.get_attribute('src')
    page.emulate_media(color_scheme='dark')
    assert video.get_attribute('src') == source
    assert video.evaluate('(v) => getComputedStyle(v).backgroundColor') == 'rgb(17, 20, 24)'
    page.goto(base + '/animations/plasma-oscillation.html')
    video = page.locator('video')
    assert video.evaluate('(v) => v.paused'), 'Reduced motion must disable standalone autoplay'
    video.click(); page.wait_for_function('document.querySelector("video").currentTime > 0.3')
    video.click(); assert video.evaluate('(v) => v.paused')
    assert not page.evaluate('Boolean(document.fullscreenElement)')
    page.goto(base + '/chapters/03-debye-shielding.html')
    plot = page.locator('picture.themed-plot').first
    for theme in ('light', 'dark'):
        page.emulate_media(color_scheme=theme)
        page.wait_for_timeout(150)
        plot.screenshot(path=str(artifacts / ('plot-' + theme + '.png')))
        chosen = plot.locator('img').evaluate('(img) => img.currentSrc')
        if theme == 'light': light = chosen
        else: assert chosen != light, 'Dark plot did not switch SVG appearance'
    context.close()
    fallback = browser.new_context(java_script_enabled=False, reduced_motion='reduce')
    fallback.route('https://cloud.tugraz.at/**/animations/*.mp4*', stream)
    page = fallback.new_page(); page.goto(base + '/animations/plasma-oscillation.html')
    assert page.locator('video').evaluate('(v) => v.controls && v.paused')
    assert page.locator('figcaption').inner_text().strip()
    assert page.locator('.animation-controls').is_hidden()
    fallback.close()
    return {'inline_click_play_pause': 'pass', 'keyboard_seek': 'pass', 'controls_fade_under_one_second': 'pass', 'explicit_native_fullscreen': full, 'full_window_fallback': window, 'no_download': True, 'theme_switch': 'pass', 'no_js_fallback': 'pass'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base', default='http://127.0.0.1:43344')
    parser.add_argument('--media', type=Path, required=True)
    parser.add_argument('--artifacts', type=Path, required=True)
    parser.add_argument('--browser', choices=('chromium', 'webkit'), default='chromium')
    parser.add_argument('--executable')
    parser.add_argument('--ipad', action='store_true')
    args = parser.parse_args(); args.artifacts.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        options = {'headless': True}
        if args.executable: options['executable_path'] = args.executable
        browser = getattr(p, args.browser).launch(**options)
        try:
            result = audit(browser, args.base.rstrip('/'), args.media, args.artifacts, p.devices['iPad Pro 11'] if args.ipad else None)
            print(json.dumps(result))
        finally:
            browser.close()
