from langchain_core.tools import tool
from dotenv import load_dotenv
import time
from typing import Optional
from playwright.sync_api import sync_playwright
from pathlib import Path
import os

_playwright = None
_page = None
_browser = None

def _get_page():
    """Retrieve existing page or launch Chromium with bot-detection bypass."""
    global _playwright, _context, _page
    if _page is None or _page.is_closed():
        _playwright = sync_playwright().start()

        # Store profile/cache locally to appear as a regular returning user
        user_data_dir = (
            Path(__file__).resolve().parents[2] / ".browser_profile"
        )
        os.makedirs(user_data_dir, exist_ok=True)

        _context = _playwright.chromium.launch_persistent_context(
            user_data_dir=str(user_data_dir),
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--no-sandbox",
            ],
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        )
        _page = _context.pages[0] if _context.pages else _context.new_page()

    return _page


def _try_skip_ad(page, max_wait_seconds: int = 7):
    """Wait for YouTube ad skip countdown to finish and click Skip."""
    skip_selectors = [
        "button.ytp-skip-ad-button",
        "button.ytp-ad-skip-button-modern",
        ".ytp-ad-skip-button",
        ".ytp-ad-skip-button-container",
    ]

    start_time = time.time()
    while time.time() - start_time < max_wait_seconds:
        # Check if an ad is currently playing
        is_ad = page.locator(".ad-showing, .ytp-ad-player-overlay").count() > 0
        if not is_ad:
            return False  # No ad running, exit early

        for selector in skip_selectors:
            btn = page.locator(selector).first
            try:
                if btn.is_visible():
                    btn.click()
                    time.sleep(0.5)
                    return True
            except Exception:
                pass
        time.sleep(0.5)
    return False

@tool
def control_youtube(action : str, query : Optional[str] = None, seconds : Optional[int] = None) -> str:
    """Control youtube playback on local desktop brower.

    Args:
        action : Action to run allowed values : 
        'play' (search keywords or navigate to a direct YouTube URL),
                'toggle_pause' (pause or resume playback),
                'forward' (skip forward in the video),
                'rewind' (rewind in the video),
                'next' (skip to the next video),
                'skip_ad' (attempt to skip an active ad).
        query: Search keywords (e.g., 'trending telugu music') OR a direct YouTube URL (e.g., 'https://www.youtube.com/watch?v=...'). Required if action is 'play'.
        seconds: Seconds to skip or rewind (defaults to 10 if omitted).
    """

    page = _get_page()


    try:

        if action == "play":

            if not query:
                return "Error : action play requires a query or url argument."

            if query.startswith("https://") or query.startswith("http://"):
                page.goto(query)
                page.wait_for_load_state("domcontentloaded")
                time.sleep(2)
                
                _try_skip_ad(page)

                return f"Playing direct youtube url : {query}"
            else:
                search_url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
                page.goto(search_url)
                page.wait_for_load_state("domcontentloaded")

                first_video = page.locator("ytd-video-renderer #video-title").first
                first_video.wait_for(timeout=7000)
                first_video.click()
                time.sleep(2)
                
                _try_skip_ad(page)

                return  f"Playing youtube video for search {query}."   

        elif action == "toggle_pause":
            page.keyboard.press("k")
            return "Toggle play/pause on current youtube video."

        elif action == "forward":
            press_count = max(1, (seconds or 30) // 10)
            for _ in range(press_count):
                page.keyboard("l")
                time.sleep(0.2)
            return f"Skipped forward by {press_count * 10} seconds."

        elif action == "rewind":
            press_count = max(1, (seconds or 20) // 10)
            for _ in range(press_count):
                page.keyboard.press("j")
                time.sleep(0.2)
            return f"Rewond by {press_count * 10} seonds"

        elif action == "next":
            page.keyboard.press("Shift+N")
            return "Skipped to next video."

        elif action == "skip_ad":
            skipped = _try_skip_ad(page)
            if skipped:
                return "Successfully skipped youtube ad."
            return "No skipable ad button found on screen."

        else :
            return f"Unknown action : '{action}'. Allowed actinos are play, forward, rewind, next, and skip_ad "
        
    except Exception as e:
        return f"Brower automation error : {str(e)}"