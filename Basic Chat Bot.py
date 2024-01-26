'''
A Simple Chat Bot with a Mulit-Response Generating usin random.choice 
and Google Searchusing Web Scraping methon with Beautiful Soup, 
and a Decent GUI with Tkinter.
'''


import random
import tkinter as tk
from tkinter import Scrollbar
from bs4 import BeautifulSoup
import requests


# Define intents and responses
INTENTS= {
    "hi" : ["Hello!", "Hi there!", "Hey! How can I help you?"],
    "hello" : ["Hello!", "Hi there!", "Hey! How can I help you?"],
    "greetings": ["Hello!", "Hi there!", "Hey! How can I help you?"],
    "goodbye": ["Goodbye!", "See you later!", "Have a great day!"],
    "faq": ["I'm sorry, I don't have that information right now."],
    "thanks": ["You're welcome!", "No problem!", "Happy to help!"]
}


def google_search(query, num_results=5):
    search_url = f"https://www.google.com/search?q={query}"
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    search_results = soup.find_all("div", class_="BNeawe")
    top_results = [result.text for result in search_results[:num_results]]
    return top_results

def get_response(intent):
    if intent.lower() in INTENTS:
        responses = INTENTS[intent]
        return random.choice(responses)
    else:
        google = google_search(intent, 5) # you can adjust the number of results
        if not google:
            return "I'm sorry, I don't have that information right now. \n\n"
        
        elif len(google) < 10:  
            more_results = google_search(intent, num_results=3) 
            if len(more_results) > 70:
                result_text = "\n".join(more_results)
            else:
                result_text = "\n".join(more_results)
            return result_text
        
        elif len(google) < 2:
            return f"I'm sorry, I am able to get the detials for {intent} \n\n"
        else:
            return random.choice(google)
        
def chat(event=None):
    user_input = user_entry.get().lower()
    response = get_response(user_input)
    chat_display.config(state=tk.NORMAL)
    
    # Display user message in blue
    chat_display.insert(tk.END, "You: ", "user")
    chat_display.insert(tk.END, f"{user_input}\n", "user_text")

    # Display bot message in green
    chat_display.insert(tk.END, "Chatbot: ", "bot")
    chat_display.insert(tk.END, f"{response}\n", "bot_text")
    
    chat_display.config(state=tk.DISABLED)
    user_entry.delete(0, tk.END)
    chat_display.see(tk.END)  # Auto-scroll to the bottom

# Create the GUI window
window = tk.Tk()
window.title("Simple Chatbot")
window.geometry("400x500")
window.resizable(0, 0)  # Make the window non-resizable

# Create a title label
title_label = tk.Label(window, text="Chatbot")
title_label.config(font=("Helvetica", 24))
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Create a chat display with a scrollbar
chat_display_frame = tk.Frame(window)
chat_display_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

chat_display = tk.Text(chat_display_frame, wrap=tk.WORD)
chat_display.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar = Scrollbar(chat_display_frame, command=chat_display.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_display.config(yscrollcommand=scrollbar.set)
chat_display.config(state=tk.DISABLED)

# Create a user input field
user_entry = tk.Entry(window, width=30)
user_entry.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
user_entry.bind("<Return>", chat)  # Bind Enter key to the chat function

# Create a Send button (smaller)
send_button = tk.Button(window, text="Send", command=chat, width=10)
send_button.grid(row=2, column=1, padx=10, pady=10, sticky="e")

# Configure grid row and column weights for resizing
window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=0)  # Prevent Send button from resizing

# Define text styles (colors)
chat_display.tag_configure("user", foreground="blue")
chat_display.tag_configure("user_text", foreground="black")
chat_display.tag_configure("bot", foreground="green")
chat_display.tag_configure("bot_text", foreground="black")

# Initial chatbot welcome message
chat_display.config(state=tk.NORMAL)
chat_display.insert(tk.END, "Welcome! How can I assist you?\n", "bot_text")
chat_display.config(state=tk.DISABLED)

# Run the GUI
window.mainloop()
