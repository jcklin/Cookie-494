from cookie import (
    WEBSITES,
    OUT_CSV,
    get_buttons,
    before_choice,
    clicking_button,
    write_cookies_to_csv,
)

if __name__ == "__main__":

    first_website = True

    # Loop through the list of websites and reset the header writer
    for website in WEBSITES:
        # Get the buttons and just dump to console
        print(f"\n{'='*50}")
        print(f"Processing: {website}")
        print(f"{'='*50}")

        buttons = get_buttons(website)
        print(f"Cookie buttons found: {buttons}")

        # Get three lists with cookies of this website.
        cookies_before_choice = before_choice(website)

        # Find accept-like and reject-like buttons from discovered buttons
        accept_btn = None
        reject_btn = None
        for _, text in buttons:
            lower = text.strip().lower()
            if accept_btn is None and any(k in lower for k in ["accept", "allow", "agree"]):
                accept_btn = text
            if reject_btn is None and any(k in lower for k in ["reject", "decline", "deny", "necessary only", "essential only", "required only"]):
                reject_btn = text

        # Get button text.
        print(f"Accept button: {accept_btn}")
        print(f"Reject button: {reject_btn}")

        # Click the discovered buttons
        cookies_after_accept = clicking_button(website, accept_btn) if accept_btn else []
        cookies_after_reject = clicking_button(website, reject_btn) if reject_btn else []

        # Write in CSV file!
        write_cookies_to_csv(
            OUT_CSV,
            website,
            cookies_before_choice,
            cookies_after_accept,
            cookies_after_reject,
            accept_btn or "",
            reject_btn or "",
            write_header=first_website,
        )
        first_website = False

    print(f"Saved cookie data to {OUT_CSV}")
