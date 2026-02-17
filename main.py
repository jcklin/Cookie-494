from cookie import (
    WEBSITE,
    OUT_CSV,
    get_buttons,
    before_choice,
    clicking_button,
    write_cookies_to_csv,
)

if __name__ == "__main__":
    # Get the buttons and just dump to console
    buttons = get_buttons(WEBSITE)
    print(buttons)
    
    # Get three lists with cookies of this website.
    cookies_before_choice = before_choice(WEBSITE)
    cookies_after_accept = clicking_button(WEBSITE, "accept")
    cookies_after_reject = clicking_button(WEBSITE, "decline")

    # Get button text.
    accept_button_text = "Accept"
    reject_button_text = "Decline"

    # Write in CSV file!
    write_cookies_to_csv(
        OUT_CSV,
        WEBSITE,
        cookies_before_choice,
        cookies_after_accept,
        cookies_after_reject,
        accept_button_text,
        reject_button_text,
    )

    print(f"Saved cookie data to {OUT_CSV}")
