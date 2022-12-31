import random, sys, uuid
from datetime import datetime
from app_database import Database

#Database
DATABASE_PATH = r"./dicesim.db"

#Runs the actual simulation
def run_sim(iterations):
    #Setup Database Connection
    db = Database(DATABASE_PATH)

    roll_session_id = uuid.uuid4()

    for i in range(0,iterations):
        print(f'...Roll {i}')
        roll_one = random.randint(1,6)
        roll_two = random.randint(1,6)
        time_stamp = datetime.now().timestamp()
        db.add_roll({
            'roll_session_id' : roll_session_id,
            'die_one_result' : roll_one,
            'die_two_result' : roll_two,
            'date_time_roll' : time_stamp
        })
    print(f'Finished rolling 2 dice {iterations} times.')

def manage_sessions():
    db = Database(DATABASE_PATH)
    sessions = db.get_roll_sessions()
    sessions = { x[0] + 1 : x[1] for x in list(enumerate(sessions)) }
    print('id','date/time from/to                         ', 'Number of Rolls')
    for k in sessions.keys():
        #Date time conversions
        start_time = datetime.fromtimestamp(int(round(float(sessions[k]['start_time']))))
        end_time = datetime.fromtimestamp(int(round(float(sessions[k]['end_time']))))
        print(k, start_time, ' - ',  end_time, sessions[k]['rolls'])
    selected_id = input("Select session:")
    session_id = sessions[int(selected_id)]['roll_session_id']
    no_of_rolls = sessions[int(selected_id)]['rolls']
    rolls = db.get_rolls(session_id,no_of_rolls)
    print('Dice Result:' +'\t', 'ROLLS:'+'\t\t','Percentage Rolled:'+'\t\n')
    for roll in rolls:
        print(f'''{roll['dice_no']}\t\t{roll['rolls']}\t\t{roll['percent']}\t\t\n''')

def main ():
    args = sys.argv

    if 'runsim' in args:
        #Collect the number of iterations if specified, else default to 100
        try:
            iterations = int(args[2])
        except:
            iterations = 100
        run_sim(iterations)
    if 'sessions' in args:
        manage_sessions()
 
if __name__ == '__main__':
    main()