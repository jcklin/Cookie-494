from cookie import (
    WEBSITES,
    OUT_CSV,
    get_buttons,
    before_choice,
    clicking_button,
    write_cookies_to_csv,
)
from cookie_keywords import (
    ACCEPT_KEYWORDS,
    REJECT_KEYWORDS,
    SPECIAL_KEYWORDS,
    CUSTOMIZE_KEYWORDS,
)

if __name__ == "__main__":

    first_website = True

    # Loop through the list of websites and reset the header writer
    for website in WEBSITES:
        # Get the buttons and just dump to console
        print(f"\n{'='*50}")
        print(f"Processing: {website}")
        print(f"{'='*50}")

        # Get buttons.
        buttons = get_buttons(website)
        print(f"Cookie buttons found: {buttons}")

        # Get three lists with cookies of this website.
        cookies_before_choice = before_choice(website)

        # Sort buttons into different category.
        accept_btn = reject_btn = special_btn = customize_btn = None
        for _, text in buttons:
            lower = text.strip().lower()

            # Priority matters:
            # special > reject > customize > accept
            if special_btn is None and any(k in lower for k in SPECIAL_KEYWORDS):
                special_btn = text
                continue

            if reject_btn is None and any(k in lower for k in REJECT_KEYWORDS):
                reject_btn = text
                continue

            if customize_btn is None and any(k in lower for k in CUSTOMIZE_KEYWORDS):
                customize_btn = text
                continue

            if accept_btn is None and any(k in lower for k in ACCEPT_KEYWORDS):
                accept_btn = text

        # Get button text.
        print(f"Accept button: {accept_btn}")
        print(f"Reject button: {reject_btn}")
        print(f"Special button: {special_btn}")
        print(f"Customize button: {customize_btn}")

        # Click the discovered buttons
        cookies_after_accept = clicking_button(website, accept_btn) if accept_btn else []
        cookies_after_reject = clicking_button(website, reject_btn) if reject_btn else []
        cookies_after_special = clicking_button(website, special_btn) if special_btn else []

        # Write in CSV file!
        write_cookies_to_csv(
            OUT_CSV,
            website,
            cookies_before_choice,
            cookies_after_accept,
            cookies_after_reject,
            cookies_after_special,
            accept_btn or "",
            reject_btn or "",
            special_btn or "",
            write_header=first_website,
        )
        first_website = False

        print(f"Saved cookie data to {OUT_CSV} from {website}")
    
