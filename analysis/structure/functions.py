import datetime
import dateutil.parser 
import json
import argparse
import os
import pickle
from collections import defaultdict


def time_parser(data_json):
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', action='store')
    filename = data_json
    with open(filename) as f:
        json_data = json.load(f)
    for i in (json_data):
        i['ts'] = dateutil.parser.isoparse(i['ts']) # ISO 8601 extended format
    return json_data


def find_interaction(to, fro):
    chat_logs = time_parser('../../data/logs/chat_logs.json')
    jabber_logs = time_parser('../../data/logs/jabber_logs.json')
    messages = {}
    with open('../../data/user_lists/users.txt') as f:
        users = f.read().splitlines()
    for i in users:
        messages[i] = {}
    for i in users:
        for j in users:
            messages[i][j] = []
    for i in chat_logs:
        sender = i['from']
        receiver = i['to']
        messages[sender][receiver].append(i['ts'])
    for i in jabber_logs:
        sender = i['from']
        receiver = i['to']
        messages[sender][receiver].append(i['ts'])
    for i in messages.keys():
        for j in messages[i].keys():
            messages[i][j] = sorted(messages[i][j])
    return messages[to][fro]


def find_users(user_fp):
    users = []
    with open(user_fp) as f:
        users = f.read().splitlines()
    return users

def all_conversations_sorted():
    # Step 0: Load alias mapping from a JSON file (adjust the path as needed)
    try:
        with open("../../data/logs/user match list.json", "r") as f:
            alias_list = json.load(f)
    except Exception as e:
        print("Failed to load alias mapping:", e)
        alias_list = []
    
    # Build a dictionary mapping each alias (and primary) to its canonical primary name.
    alias_mapping = {}
    for entry in alias_list:
        primary = entry.get('primary')
        if primary:
            alias_mapping[primary] = primary  # Map the primary to itself.
            for alias in entry.get('aliases', []):
                alias_mapping[alias] = primary

    # Step 1: Count messages in JSON logs
    chat_logs = time_parser('../../data/logs/chat_logs.json')
    jabber_logs = time_parser('../../data/logs/jabber_logs.json')
    structured_messages = {}  # dict to store conversations

    initial_count = len(chat_logs) + len(jabber_logs)
    print(f"Initial total message count: {initial_count}")

    def extract_conversations(logs):
        for i in logs:
            # Get raw sender/receiver values from the log
            sender = i['from']
            receiver = i['to']

            # Normalize using alias mapping if the name is an alias
            sender_canonical = alias_mapping.get(sender, sender)
            # if sender_canonical != sender:
            #     print(f"Sender: {sender} -> Canonical: {sender_canonical}")
            receiver_canonical = alias_mapping.get(receiver, receiver)
            # if receiver_canonical != receiver:
            #     # Print only if the mapping is different
            #     print(f"Receiver: {receiver} -> Canonical: {receiver_canonical}")

            # Use sorted keys for uniqueness (order-independent conversation key)
            key1, key2 = sorted([sender_canonical, receiver_canonical])
            if key1 not in structured_messages:
                structured_messages[key1] = {}
            if key2 not in structured_messages[key1]:
                structured_messages[key1][key2] = []
            structured_messages[key1][key2].append((i['ts'], sender_canonical, receiver_canonical, i['body']))

    extract_conversations(chat_logs)
    extract_conversations(jabber_logs)

    # Step 2: Count messages in structured_messages
    processed_count = sum(len(convo) for user in structured_messages.values() for convo in user.values())
    print(f"Total processed message count: {processed_count}")

    # Sorting each conversation by time (assuming timestamp is the first tuple element)
    for user in structured_messages.keys():
        for convo in structured_messages[user].keys():
            structured_messages[user][convo].sort(key=lambda x: x[0])

    if initial_count != processed_count:
        print(f"Mismatch detected! Initial count: {initial_count}, Processed count: {processed_count}")
    else:
        print("Message counts match.")

    return structured_messages

def count_files_in_folder(folder_path):
    try:
        # List all items in the directory and filter for files
        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        return len(files)
    except FileNotFoundError:
        print("Folder not found.")
        return 0
    
def split_to_txt_files(conversations_dict, save_to_path):
    # Ensure the directory structure exists
    if not os.path.exists(save_to_path):
        os.makedirs(save_to_path)

    for user_i in conversations_dict.keys():
        for user_j in conversations_dict[user_i].keys():
            # Create file for each 1-1 conversation 
            output_file_path = f'{save_to_path}{user_i}<>{user_j}.txt'
            
            # Write each message to the text file
            with open(output_file_path, 'w', encoding='utf-8') as txt_file:
                txt_file.write("Timestamp\tFrom\tTo\tMessage\n")  # Header row
                for message in conversations_dict[user_i][user_j]:
                    ts, from_user, to_user, body = message
                    txt_file.write(f"{ts}\t{from_user}\t{to_user}\t{body}\n")


def count_unique_users_in_conversations(conversations_dict):
    users = set()
    for user_i, user_j_convos in conversations_dict.items():
        # Add user_i only once
        users.add(user_i)
        # Add each user_j from the nested dictionary of user_i
        users.update(user_j_convos.keys())
    return len(users)

def save_graph(graph, filename):
    with open(filename, "wb") as f:
        pickle.dump(graph, f)
    print(f"Graph saved as {filename}")

def load_graph(filename):
    with open(filename, "rb") as f:
        graph = pickle.load(f)
    print(f"Graph loaded from {filename}")
    return graph

def filter_single_speaker_conversations(conversations_dict):
    single_speaker_conversations = {}
    
    for user_i in conversations_dict.keys():
        for user_j, messages in conversations_dict[user_i].items():
            # Get the set of unique senders in the conversation
            unique_senders = {message[1] for message in messages}
            
            # If there's only one unique sender, add to the filtered dict
            if len(unique_senders) == 1:
                if user_i not in single_speaker_conversations:
                    single_speaker_conversations[user_i] = {}
                single_speaker_conversations[user_i][user_j] = messages
                
    return single_speaker_conversations

def count_conversations(conversations_dict):
    total_count = 0
    for user_i in conversations_dict.keys():
        total_count += len(conversations_dict[user_i])  # Count each conversation between user_i and user_j
    return total_count

def filter_two_way_conversations(conversations_dict, single_speaker_conversations):
    # Create a new dictionary with only two-way conversations
    two_way_conversations = {}
    
    for user_i in conversations_dict.keys():
        for user_j in conversations_dict[user_i].keys():
            # Check if this conversation is not in single_speaker_conversations
            if user_i not in single_speaker_conversations or user_j not in single_speaker_conversations[user_i]:
                if user_i not in two_way_conversations:
                    two_way_conversations[user_i] = {}
                two_way_conversations[user_i][user_j] = conversations_dict[user_i][user_j]
    
    return two_way_conversations

def filter_out_glitch_conversations(conversations_dict):
    valid_conversations = {}
    
    for user_i in conversations_dict.keys():
        for user_j, messages in conversations_dict[user_i].items():
            # Assume conversation is valid unless it matches a glitch pattern
            is_glitch = False

            # Check if the conversation length is 2 or 4 and matches glitch criteria
            if len(messages) == 2:
                # Glitch pattern for 2-message conversation
                if messages[0][1] == user_i and messages[1][1] == user_j and messages[0][3] == messages[1][3]:
                    is_glitch = True

            elif len(messages) == 4:
                # Glitch pattern for 4-message conversation
                if (messages[0][1] == user_i and messages[1][1] == user_i and
                    messages[2][1] == user_j and messages[3][1] == user_j and
                    messages[0][3] == messages[2][3] and messages[1][3] == messages[3][3]):
                    is_glitch = True

            # If not a glitch, add to valid conversations
            if not is_glitch:
                if user_i not in valid_conversations:
                    valid_conversations[user_i] = {}
                valid_conversations[user_i][user_j] = messages
                
    return valid_conversations

def remove_encrypted_messages(conversations_dict):
    """
    Removes messages that contain '[Ошибка: сообщение зашифровано, и невозможно его расшифровать.]'
    from the conversation dataset and counts the number of messages before and after removal.

    Parameters:
        conversations_dict (dict): Nested dictionary of conversations.
                                   Format: {user_i: {user_j: messages, ...}, ...}

    Returns:
        tuple:
            - dict: A new conversation dictionary with encrypted messages removed.
            - int: Total number of messages before removal.
            - int: Total number of messages after removal.
    """
    filtered_conversations = {}
    total_before = 0
    total_after = 0

    for user_i, threads in conversations_dict.items():
        filtered_threads = {}

        for user_j, messages in threads.items():
            total_before += len(messages)  # Count messages before removal

            # Filter messages that do not contain the encrypted error message
            filtered_messages = [
                msg for msg in messages if msg[3] != "[Ошибка: сообщение зашифровано, и невозможно его расшифровать.]"
            ]

            total_after += len(filtered_messages)  # Count messages after removal

            # Only add the thread if there are remaining messages
            if filtered_messages:
                filtered_threads[user_j] = filtered_messages

        # Only add user conversations if there are remaining threads
        if filtered_threads:
            filtered_conversations[user_i] = filtered_threads

    return filtered_conversations, total_before, total_after

def segment_conversations_by_date(conversations_dict):
    """
    Splits all conversations into units where each unit contains messages from the same day.

    Parameters:
        conversations_dict (dict): Nested dictionary of conversations.
                                   Format: {user_i: {user_j: messages, ...}, ...}

    Returns:
        conversation_segments (dict): Dictionary with conversation segments split by date.
                                      Format: {(user_i, user_j): [conversation_units]}
    """
    conversation_segments = {}

    for user_i, threads in conversations_dict.items():
        for user_j, messages in threads.items():
            # Group messages by date
            conversation_units = defaultdict(list)
            for msg in messages:
                msg_date = msg[0].date()  # Extract the date from the timestamp
                conversation_units[msg_date].append(msg)

            # Store the segmented conversation
            conversation_segments[(user_i, user_j)] = list(conversation_units.values())

    return conversation_segments

def split_into_speaking_turns(conversation_units):
    """
    Splits conversation units into speaking turns. Each turn contains consecutive 
    messages from the same user. A new turn starts when:
      - The sender changes, OR
      - The same sender sends a message more than 30 minutes after their previous message.
      
    Parameters:
        conversation_units (dict): A dictionary where:
            - Keys: (user_i, user_j) tuples representing a conversation.
            - Values: A list of conversation units (each unit is a list of messages).
              Each message is assumed to be a tuple (timestamp, sender, receiver, body).
    
    Returns:
        conversation_turns (dict): A dictionary where:
            - Keys: (user_i, user_j) tuples.
            - Values: A list of conversation units, each now split into speaking turns.
                      Each speaking turn is a list of messages.
    """
    conversation_turns = {}

    # Iterate over each conversation identified by a pair (user_i, user_j)
    for (user_i, user_j), units in conversation_units.items():
        new_units = []  # For storing all turn-split units within this conversation

        for unit in units:
            if not unit:
                continue  # Skip empty units if any

            current_turn = [unit[0]]  # Start with the first message in the unit
            turns = []

            # Go through each subsequent message in the unit
            for i in range(1, len(unit)):
                curr_msg = unit[i]
                prev_msg = unit[i - 1]
                
                # Check if the sender has changed OR if the time difference is more than 30 minutes.
                # It is assumed that the first element of the message tuple is a numeric timestamp.
                if curr_msg[1] != prev_msg[1] or ((curr_msg[0] - prev_msg[0]).total_seconds() > 1800):
                    # Save the finished turn and start a new one.
                    turns.append(current_turn)
                    current_turn = [curr_msg]
                else:
                    # Same sender and less than 30 minutes apart: continue the same turn.
                    current_turn.append(curr_msg)

            # Append the final current turn for this unit.
            if current_turn:
                turns.append(current_turn)

            new_units.append(turns)

        conversation_turns[(user_i, user_j)] = new_units

    return conversation_turns
