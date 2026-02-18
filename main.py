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
        cookies_after_accept = clicking_button(website, "accept")
        cookies_after_reject = clicking_button(website, "decline")

        # Get button text.
        accept_button_text = "Accept"
        reject_button_text = "Decline"

        # Write in CSV file!
        write_cookies_to_csv(
            OUT_CSV,
            website,
            cookies_before_choice,
            cookies_after_accept,
            cookies_after_reject,
            accept_button_text,
            reject_button_text,
            write_header=first_website,
        )
        first_website = False

    print(f"Saved cookie data to {OUT_CSV}")
