import pyrebase
from flask import Flask, render_template, request, redirect, url_for, session
import random
import time

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = 'your_secret_key'  # Change this to a secure random value

# Firebase config
config = {
    "apiKey": "AIzaSyDPjTR7oBLHePEULuNX7Mtb838CRWzYjt4",
    "authDomain": "speed-typing-6b503.firebaseapp.com",
    "databaseURL": "https://speed-typing-6b503-default-rtdb.firebaseio.com/",
    "projectId": "speed-typing-6b503",
    "storageBucket": "speed-typing-6b503.appspot.com",
    "messagingSenderId": "1057263183786",
    "appId": "1:1057263183786:web:5b26f65f4b4d33e6dcadd3",
    "measurementId": "G-PMPX7TKYES"
}

try:
    firebase = pyrebase.initialize_app(config)
    auth = firebase.auth()
    db = firebase.database()
    print("Firebase initialized successfully")  # Debug print
except Exception as e:
    print(f"Firebase initialization error: {str(e)}")  # Debug print
    firebase = None
    auth = None
    db = None

# Typing test logic
paragraphs = [
    "Yesterday I saw a film titled Macbeth. Its story elements are interesting. The film's hero, Macbeth, assassinates Duncan and ascends to the throne of Scotland. But he is dissatisfied. He finds himself in a dangerous situation. He executes those he suspects of plotting against him. Eventually, some of the lords revolted and dethroned him and killed him. The message it conveys is that excessive ambition destroys a man. The actor and actress who played Macbeth and Lady Macbeth had exceptional performances, which significantly increased the film's impact.",
    "Everyone knows that paper is made from trees. But when one looks at trees, one cannot imagine that something so soft and fragile as the paper is made is so hard and strong. Plant materials such as wood are made of fibres known as cellulose. It is the primary ingredient in paper making. Raw wood is first converted into pulp consisting of a mixture of Cellulose, lignin, water and some chemicals. The pulp can be made mechanically through grinders or through chemical processes. Short fibres are produced by mechanical grinding. The paper produced in this way is weak and is used to make newspapers, magazines and phonebooks.",
    'The ant and the grasshopper were good friends. In the summer, the ant works hard to fill his storage with food. While the grasshopper was enjoying the fine weather and playing all day. When winter came, the ant was lying cozily in his home surrounded by the food he stored during the summer. While the grasshopper was in his home, hungry and freezing. He asked the ant for food and the ant gave him some. But it wasn\'t enough to last the entire winter. When he tried to ask the ant again, the latter replied: "I\'m sorry my friend but my food is just enough for my family to last until the end of winter. If I give you more, we too will starve. We had the entire summer to prepare for the winter but you chose to play instead."',
    'There was once a shepherd boy who liked to play tricks. One day, while he was watching over the herd, the boy decided to play a trick and cried "wolf! wolf!". The people who heard rushed over to help him. But they were disappointed when they saw that there was no wolf and the boy was laughing at them. The next day, he did it again and people rushed to his aid only to be disappointed once again. On the third day, the boy saw a wolf devouring one of his sheep and cried for help. But the people who heard him thought this is just another of the boy\'s pranks so no one came to help him. That day, the boy lost some of his sheep to the wolf.',
    "Most of us have probably heard of this story as this is one of the most popular fairy tales in the world. The story revolves around a duckling who from the moment of his birth has always felt different from his siblings. He was always picked on because he didn't look like the rest of them. One day, he had enough and ran away from the pond he grew up in. He wandered near and far looking for a family who would accept him. Months passed and seasons changed but everywhere he went, nobody wanted him because he was such an ugly duck. Then one day, he came upon a family of swans. Upon looking at them, he realized that during the months he spent looking for a family to call his own, he had grown into a beautiful swan. Now he finally understood why he never looked like the rest of his siblings because he isn't a duck but a swan.",
    "A lion was once sleeping in the jungle when a mouse started running up and down his body just for fun. This disturbed the lion's sleep, and he woke up quite angry. He was about to eat the mouse when the mouse desperately requested the lion to set him free. 'I promise you, I will be of great help to you someday if you save me.' The lion laughed at the mouse's confidence and let him go. One day, a few hunters came into the forest and took the lion with them. They tied him up against a tree. The lion was struggling to get out and started to whimper. Soon, the mouse walked past and noticed the lion in trouble. Quickly, he ran and gnawed on the ropes to set the lion free. Both of them sped off into the jungle.",
    "One day, a selfish fox invited a stork for dinner. Stork was very happy with the invitation – she reached the fox's home on time and knocked at the door with her long beak. The fox took her to the dinner table and served some soup in shallow bowls for both of them. As the bowl was too shallow for the stork, she couldn't have soup at all. But, the fox licked up his soup quickly. The stork was angry and upset, but she didn't show her anger and behaved politely. To teach a lesson to the fox, she then invited him for dinner the next day. She too served soup, but this time the soup was served in two tall narrow vases. The stork devoured the soup from her vase, but the fox couldn't drink any of it because of his narrow neck. The fox realised his mistake and went home famished.",
    "Once there lived a greedy man in a small town. He was very rich, and he loved gold and all things fancy. But he loved his daughter more than anything. One day, he chanced upon a fairy. The fairy's hair was caught in a few tree branches. He helped her out, but as his greediness took over, he realised that he had an opportunity to become richer by asking for a wish in return (by helping her out). The fairy granted him a wish. He said, 'All that I touch should turn to gold.' And his wish was granted by the grateful fairy. The greedy man rushed home to tell his wife and daughter about his wish, all the while touching stones and pebbles and watching them convert into gold. Once he got home, his daughter rushed to greet him.",
    "Patty, a milkmaid milked her cow and had two full pails of fresh, creamy milk. She put both pails of milk on a stick and set off to the market to sell the milk. As she took steps towards the market, her thoughts took steps towards wealth. On her way, she kept thinking about the money she would make from selling the milk. Then she thought about what she would do with that money. She was talking to herself and said, 'Once I get the money, I'll buy a chicken. The chicken will lay eggs and I will get more chickens. They'll all lay eggs, and I will sell them for more money. Then, I'll buy the house on the hill and everyone will envy me.' She was very happy that soon she would be very rich. With these happy thoughts, she marched ahead.",
    "Nasir, a small boy, found a crystal ball behind the banyan tree of his garden. The tree told him that it would grant him a wish. He was very happy and he thought hard, but unfortunately, he could not come up with anything he wanted. So, he kept the crystal ball in his bag and waited until he could decide on his wish. Days went by without him making a wish but his best friend saw him looking at the crystal ball. He stole it from Nasir and showed it to everyone in the village. They all asked for palaces and riches and lots of gold, but could not make more than one wish. In the end, everyone was angry because no one could have everything they wanted. They became very unhappy and decided to ask Nasir for help."
]
selected_paragraph = random.choice(paragraphs)
timer_duration = 120
start_time = None
num_words_typed = 0
num_correct_characters = 0
accuracy = 0
elapsed_time = 0

# Add a simple test route
@app.route('/test')
def test():
    return "Flask is working! Firebase status: " + ("Connected" if auth is not None else "Not connected")

# Auth routes
@app.route('/')
def login():
    if 'is_logged_in' in session and session['is_logged_in']:
        return redirect(url_for('typing_test'))
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        name = request.form['name']
        try:
            if auth is None:
                print("Firebase auth not initialized")
                return redirect(url_for('signup'))
            print(f"Attempting to create user: {email}")  # Debug print
            auth.create_user_with_email_and_password(email, password)
            print(f"User created in Firebase Auth: {email}")  # Debug print
            user = auth.sign_in_with_email_and_password(email, password)
            print(f"User signed in: {email}")  # Debug print
            session['is_logged_in'] = True
            session['email'] = user['email']
            session['name'] = name
            session['uid'] = user['localId']
            print(f"Session created: {session}")  # Debug print
            # Store user data in DB
            if db is not None:
                try:
                    db.child('users').child(user['localId']).set({
                        'name': name,
                        'email': email
                    })
                    print(f"User data saved to database: {email}")  # Debug print
                except Exception as db_error:
                    print(f"Database error (but continuing): {str(db_error)}")  # Debug print
            print(f"User created successfully: {email}")  # Debug print
            print(f"Redirecting to welcome page...")  # Debug print
            return redirect(url_for('welcome'))
        except Exception as e:
            print(f"Registration error: {str(e)}")  # Debug print
            return redirect(url_for('signup'))
    else:
        return redirect(url_for('signup'))

@app.route('/result', methods=['POST', 'GET'])
def result():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pass']
        try:
            if auth is None:
                print("Firebase auth not initialized")
                return redirect(url_for('login'))
            print(f"Attempting to sign in: {email}")  # Debug print
            user = auth.sign_in_with_email_and_password(email, password)
            session['is_logged_in'] = True
            session['email'] = user['email']
            session['name'] = ''  # Optionally fetch from DB
            session['uid'] = user['localId']
            print(f"Sign in successful: {email}")  # Debug print
            return redirect(url_for('welcome'))
        except Exception as e:
            print(f"Sign in error: {str(e)}")  # Debug print
            return redirect(url_for('login'))
    else:
        if 'is_logged_in' in session and session['is_logged_in']:
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('login'))

@app.route('/welcome')
def welcome():
    print(f"Welcome route accessed. Session: {session}")  # Debug print
    if 'is_logged_in' in session and session['is_logged_in']:
        print(f"User is logged in: {session.get('email')}")  # Debug print
        history = []
        latest_result = None
        if 'uid' in session and db is not None:
            try:
                results = db.child('results').child(session['uid']).get()
                if results and results.each():
                    for item in results.each():
                        history.append(item.val())
                    # Get the latest result (most recent timestamp)
                    if history:
                        latest_result = max(history, key=lambda x: x.get('timestamp', ''))
                print(f"History fetched: {len(history)} items")  # Debug print
            except Exception as e:
                print(f"Error fetching history: {str(e)}")
        print(f"Rendering welcome template...")  # Debug print
        return render_template('welcome.html', email=session.get('email', ''), name=session.get('name', ''), history=history, latest_result=latest_result)
    else:
        print(f"User not logged in, redirecting to login")  # Debug print
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Typing test (protected)
@app.route('/typing-test')
def typing_test():
    if 'is_logged_in' not in session or not session['is_logged_in']:
        return redirect(url_for('login'))
    global selected_paragraph, start_time, num_words_typed, num_correct_characters, accuracy, elapsed_time
    selected_paragraph = random.choice(paragraphs)
    start_time = None
    num_words_typed = 0
    num_correct_characters = 0
    accuracy = 0
    elapsed_time = 0
    return render_template('index.html', paragraph=selected_paragraph, timer=timer_duration)

@app.route('/change_paragraph', methods=['POST'])
def change_paragraph():
    if 'is_logged_in' not in session or not session['is_logged_in']:
        return redirect(url_for('login'))
    global selected_paragraph
    selected_paragraph = random.choice(paragraphs)
    return selected_paragraph

@app.route('/typing-result', methods=['POST'])
def typing_result():
    if 'is_logged_in' not in session or not session['is_logged_in']:
        return redirect(url_for('login'))
    global start_time, num_words_typed, num_correct_characters
    if request.form.get('user_input') == '':
        start_time = None
        time_elapsed = 0
    if start_time is None:
        start_time = time.time()
    user_input = request.form.get('user_input', '')
    num_words_typed = len(user_input.split())
    num_correct_characters = sum(user_input[i] == selected_paragraph[i] for i in range(min(len(user_input), len(selected_paragraph))))
    time_remaining = max(0, timer_duration - (time.time() - start_time))
    time_elapsed = time.time() - start_time
    # Store typing result in DB (history)
    if 'uid' in session and db is not None:
        try:
            import datetime
            timestamp = datetime.datetime.now().isoformat()
            db.child('results').child(session['uid']).push({
                'wpm': (num_words_typed / (time_elapsed / 60)) if time_elapsed > 0 else 0,
                'accuracy': (num_correct_characters / len(selected_paragraph)) * 100,
                'time_elapsed': time_elapsed,
                'word_count': num_words_typed,
                'timestamp': timestamp
            })
        except Exception as e:
            print(f"Error saving result: {str(e)}")
    return {
        'time_remaining': time_remaining,
        'words_per_minute': (num_words_typed / (time_elapsed / 60)) if time_elapsed > 0 else 0,
        'accuracy': (num_correct_characters / len(selected_paragraph)) * 100,
        'time_elapsed': time_elapsed,
        'word_count': num_words_typed
    }

if __name__ == '__main__':
    app.run(debug=True)
