import telebot
import praw
import random

# Enter the API of your Telegram bot
BOT_TOKEN = 'Enter the API of your Telegram bot'

# Initialize the bot with your token
bot = telebot.TeleBot(BOT_TOKEN)

# Initialize the Reddit instance with your credentials
reddit = praw.Reddit(client_id='Enter the API of your Reddit client ID',
                     client_secret='Enter the API of your Reddit client secret',
                     user_agent='web:myredditbot:v1.0 (by u/your_username)')


@bot.message_handler(commands=['start'])
def welcome_message(message):
    bot.reply_to(message, "Salutations, esteemed user,\n\n"
                          "I am your devoted Reddit browsing assistant. Here are the commands you can use:\n\n"
                          "1. /start - To initiate our grand endeavor\n"
                          "2. /search +[the topic of your choice] - To fetch the 5 most pertinent posts related to your topic\n"
                          "3. /trend +[subreddit name] - To fetch the trending posts from your chosen subreddit\n"
                          "4. /help - To receive guidance on the full suite of commands at your disposal")


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "Would be my utmost pleasure to assist you,\n\n"
                          "1. /start - To initiate our grand endeavor\n"
                          "2. /search +[the topic of your choice] - To fetch the 5 most pertinent posts related to your topic\n"
                          "3. /trend +[subreddit name] - To fetch the trending posts from your chosen subreddit\n"
                          "4. /help - To receive guidance on the full suite of commands at your disposal")


# Command handler to fetch a trending post from a subreddit
@bot.message_handler(commands=['trend'])
def send_trending_post(message):
    try:
        # Extract the subreddit name from the message text
        subreddit_name = message.text.split()[1]
        subreddit = reddit.subreddit(subreddit_name)

        # Fetch the top 10 hot posts from the subreddit
        hot_posts = list(subreddit.hot(limit=10))

        # Select a random post from the top 10
        random_post = random.choice(hot_posts)

        # Send the caption as a separate message
        bot.send_message(message.chat.id, random_post.title)

        # Check if the post has an image or video and send it
        if hasattr(random_post, 'post_hint'):
            if random_post.post_hint == 'image':
                bot.send_photo(message.chat.id, random_post.url)
            elif random_post.post_hint.startswith('hosted:video'):
                bot.send_video(message.chat.id, random_post.media['reddit_video']['fallback_url'])
        else:
            # If there is no media, send the URL as a separate message
            bot.send_message(message.chat.id, random_post.url)

        bot.send_message(message.chat.id, f"Link to the post: https://www.reddit.com{random_post.permalink}")

    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")


# Command handler to search Reddit and send the top 5 results
@bot.message_handler(commands=['search'])
def send_search_results(message):
    try:
        # Extract the search query from the message text
        search_query = ' '.join(message.text.split()[1:])
        search_results = reddit.subreddit('all').search(search_query, limit=5)

        # Send the top 5 search results
        for post in search_results:
            bot.send_message(message.chat.id, f"Title: {post.title}\n"
                                              f"Subreddit: r/{post.subreddit}\n"
                                              f"Upvotes: {post.score}\n"
                                              f"Link: https://www.reddit.com{post.permalink}\n")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")


# Polling
bot.polling()
