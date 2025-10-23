"""Scrape the ServiceTitan OpenAPI specs."""  # noqa: INP001

import asyncio
from pathlib import Path

import rich
from bs4 import BeautifulSoup
from playwright.async_api import Playwright, async_playwright

DOCS_ROOT = "https://developer.servicetitan.io"
OUTPUT_DIR = Path("tap_service_titan/openapi_specs")


def get_api_name_from_url(url: str) -> str:
    """Get the API name from a URL."""
    return url.split("api=")[-1].replace("tenant-", "")


async def get_soup_from_url(
    playwright: Playwright,
    url: str,
) -> tuple[str, BeautifulSoup]:
    """Get a BeautifulSoup object from a URL."""
    rich.print(f"Getting soup from {url}")
    browser = await playwright.chromium.launch()
    page = await browser.new_page()
    page.set_default_timeout(100000)
    await page.goto(url, wait_until="networkidle")
    html = await page.content()
    return (url, BeautifulSoup(html, "html.parser"))


async def get_all_service_titan_soups() -> dict[str, BeautifulSoup]:
    """Get all ServiceTitan API docs as BeautifulSoup objects."""
    async with async_playwright() as playwright:
        _, soup = await get_soup_from_url(playwright, f"{DOCS_ROOT}/apis/")
        api_urls = [
            f"{DOCS_ROOT}{href}"
            for href in [a.get("href") for a in soup.find_all("a")]
            if "api-details" in href
        ]
        tasks = [get_soup_from_url(playwright, api_url) for api_url in api_urls]
        api_defs = await asyncio.gather(*tasks)
        return {get_api_name_from_url(url): api_doc for (url, api_doc) in api_defs}


async def download_openapi_spec(
    playwright: Playwright,
    url: str,
    download_path: Path,
) -> None:
    """Download an OpenAPI spec from a URL."""
    browser = await playwright.chromium.launch()
    page = await browser.new_page()
    page.set_default_timeout(100000)
    await page.goto(url, wait_until="networkidle")
    async with page.expect_download() as download_info:
        await page.select_option("#apiDefinitions", "openapi+json")

    download = await download_info.value
    await download.save_as(download_path)
    await browser.close()


async def download_all_openapi_specs() -> None:
    """Download all ServiceTitan OpenAPI specs."""
    async with async_playwright() as playwright:
        _, soup = await get_soup_from_url(playwright, f"{DOCS_ROOT}/apis/")
        api_urls = [
            f"{DOCS_ROOT}{href}"
            for href in [a.get("href") for a in soup.find_all("a")]
            if "api-details" in href
        ]
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        tasks = []
        for api_url in api_urls:
            download_path = OUTPUT_DIR / f"{get_api_name_from_url(api_url)}.json"
            tasks.append(download_openapi_spec(playwright, api_url, download_path))
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(download_all_openapi_specs())
