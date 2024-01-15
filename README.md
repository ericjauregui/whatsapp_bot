```markdown
# WhatsApp Bot

This is a WhatsApp bot that allows you to send messages to multiple recipients using WhatsApp Web.

## Prerequisites

- Python 3.x
- Google Chrome with WhatsApp Web signed in
- Latest chromedriver (https://chromedriver.chromium.org/downloads) and added to PATH

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/ericjauregui/whatsapp-bot.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up the recipients:

   - Create the `recipients/recipients.csv` file.
   - Fill in the contact details of the recipients you want to send messages to.

4. Configure the bot:

   - Open the `utils/utils.py` file.
   - Update the `COOKIES` variable in 'main.py' with the path to your Google Chrome cookies file.

## Usage

1. Run the bot:

   ```bash
   python main.py
   ```

2. Follow the on-screen instructions:

   - Confirm the number of recipients you want to send messages to.
   - Choose whether to include pictures from the `pictures` folder.
   - Enter your message.

3. Let the bot run without interruption.

## Folder Structure

- `recipients/`: Contains the recipients.csv file with contact details.
- `pictures/`: Place pictures you want to send here.
- `utils/`: Contains the utils.py file with utility functions.
- `main.py`: Main script to run the bot.

## Contact

For any questions or inquiries, please contact [eric.jauregui@ymail.com](mailto:eric.jauregui@ymail.com).
```