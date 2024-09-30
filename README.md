# Instagram-Scraper-Manager

Instagram-Scraper-Manager is a Python-based tool designed to scrape content from Instagram accounts and automate posting to your own Instagram account. This project utilizes **instagrapi**, **instaloader**, and **moviepy** libraries to provide a seamless experience for managing multiple accounts and automating content posting.

## Features

- **Account Management**: Easily add new Instagram accounts, manage scraping accounts, set taglines, and add captions/hashtags.
- **Automated Posting**: Post reels to single or multiple accounts with various strategies.
- **Session Management**: Avoid logging in repeatedly with saved sessions.
- **Customization**: Add margins, captions, and hashtags before posting to enhance reach.
- **Auto Reel/Feed scrolling**: Automatic reel/feed scrolling(keyword supported) to increase page value

## How to Use

1. **Account Management**:

   - Run `accounts.app.py` to manage accounts.
   - Options include adding new accounts, managing scraping accounts, and setting captions or taglines.

2. **Posting Reels**:
   - Run `poster.app.py` to post content to your Instagram accounts.
   - Select from multiple posting strategies, including posting to all accounts or to specific ones.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Poojan38380/Instagram-Scraper-Manager.git
   ```
2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Add your Instagram account(s) via `accounts.app.py` and start automating posts using `poster.app.py`.

## Modules Overview

- **accounts.app.py**: Manages Instagram accounts (adding, removing, viewing).
- **poster.app.py**: Handles posting of reels with different strategies.
- **utils**: Provides utility functions for input handling and error management.

## Contributions

We welcome contributions and collaboration! Feel free to post issues, suggest features, or submit pull requests. Let’s grow and improve this project together.

## License

This project is licensed under the MIT License.

Made with ❤️ by Poojan!
