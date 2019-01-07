import datetime

def main():
    with open('scores.csv') as infile:
        data = {}
        header = infile.readline()
        for line in infile:
            user, score, date = line.split(', ')
            year, month, day = map(int, date.split('-'))
            current_date = datetime.date(year, month, day)
            if user in data:
                data[user]['score'] += int(score)

                if data[user]['last_date'] == current_date - datetime.timedelta(days=1):
                    data[user]['streak'] += 1
                else:
                    data[user]['streak'] = 1

                data[user]['last_date'] = current_date
            else:
                data[user] = {}
                data[user]['score'] = int(score)
                data[user]['last_date'] = current_date
                data[user]['streak'] = 1

        with open('users.csv', 'w') as outfile:
            for username, userdata in data.items():
                line = '%s, %s, %s\n' % (username, userdata['score'],
                                         userdata['streak'])
                outfile.write(line)



if __name__ == '__main__':
    main()
