```markdown
# WhatsApp Bot

This repository contains the code for a WhatsApp bot built with Python. The bot can send automated messages to multiple recipients using WhatsApp Web. It also supports sending pictures along with the messages.

## Prerequisites

- Python 3.x
- Google Chrome Browser
- Signed into WhatsApp Web on Google Chrome after running the first time

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ericjauregui/whatsapp_bot.git
   ```

2. Move to repo folder and install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Ensure you're signed into WhatsApp Web on your computer.
2. Run the bot for first time setup:
   ```bash
   python main.py
   ```
3. Place pictures you want to send in the `pictures` folder.
4. Fill in the contact details of the recipients in the `recipients.csv` file located in the `recipients` folder that is generated after the first run.
5. Run the bot for full use:
   ```bash
   python main.py
   ```

6. Follow the on-screen instructions to send messages. You can choose whether to include pictures from the `pictures` folder along with the messages.

## Note

- Don't touch your computer while the bot is running!
- You can stop the program by pressing `ctrl+c`.

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes.

## Contact

For any questions or inquiries, please contact [eric.jauregui@ymail.com](mailto:eric.jauregui@ymail.com).
```