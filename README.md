# Automated Email Rejection Processor

This script automates the process of identifying and handling rejection emails in your Gmail inbox.

## Setup

1. Clone this repository:

git clone https://github.com/kemoeverlyne/Automated-Email-Rejection-Processor

```shell
cd automated-email-processor
```

2. Install the required dependencies:

```shell
pip install -r requirements.txt

```

3. Create `client_secrets.json`:

Follow the instructions [here](https://developers.google.com/gmail/api/quickstart/python) to create and download your `client_secrets.json` file.

4. Configure the script:

Open `config.py` and update the following variables:

- `EMAIL_ADDRESS`: Your Gmail email address.
- `REJECTION_KEYWORDS`: List of keywords that indicate rejection emails.

5. Test the script:

Run the script manually to ensure it's working correctly


## Automation

You can automate the execution of this script using scheduled tasks on your operating system:

- **Linux/macOS (using cron):**
- Open your terminal.
- Type `crontab -e` to edit your cron jobs.
- Add a line to schedule your script. For example, to run the script every day at 3:00 AM:
 ```
 0 3 * * * /path/to/python3 /path/to/script.py
 ```
- **Windows (using Task Scheduler):**
- Open the Task Scheduler.
- Create a new task and specify the Python interpreter and script path.
- Set the desired schedule for the task.

Remember to handle errors and add proper logging in your script for a smooth automated process.

## License

This project is licensed under the [MIT License](LICENSE).
