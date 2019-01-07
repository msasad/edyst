import random
import datetime


def main():
    START_DATE = datetime.date(2018, 12, 1)
    END_DATE = datetime.date(2019, 1, 10)
    dates = []
    for i in range(int((END_DATE - START_DATE).days)):
        dates.append((START_DATE + datetime.timedelta(days=i)).isoformat())

    for date in dates:
        number_of_users = random.randint(25, 50)
        done = []
        for n in range(number_of_users):
            user_number = random.randint(1, 150)
            if user_number in done:
                continue
            done.append(user_number)
            username = 'user%04i' % user_number
            score = random.randint(100, 500)
            print('%s, %s, %s' % (username, score, date))



if __name__ == '__main__':
    main()
