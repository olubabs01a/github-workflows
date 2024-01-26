import datetime
from sys import argv
from bs4 import BeautifulSoup
import re
from urllib import request

skillsProfileUrl = ''
limit = 3

def generate_readme_text(badges: dict, limit, timestamp):
    updates = '<!-- start latest badges --><hr />\n'    
    updates += '### **&#127882; {} Latest Badges from Google Cloud Skills Boost &#127882;**'.format(limit)
    updates += '\n_Last checked: {}_'.format(timestamp)
    updates += '\n\n'

    count = 1
    for badgeKey in badges.keys():
        completion = badges[badgeKey][1]
        column = '{}&emsp;&emsp;&emsp;'.format(badges[badgeKey][0])

        print('Badge #{} found => {}, {}\n'.format(count, badgeKey, completion))

        updates += column
        count += 1

    updates += '\n\n'
    updates += '#### &#10024; Visit full profile [here]({}) &#10024;'.format(skillsProfileUrl)
    updates += '<hr /><!-- end latest badges -->'

    # Rewrite README with new post content
    fileName = 'README.md'
    currentText = open(fileName, mode='r', encoding='utf8').read();

    badgePattern = r'<!-- start latest badges -->[\S\s]*<!-- end latest badges -->'
    matches = re.search(badgePattern, currentText)

    if matches:
        newText = re.compile(badgePattern).sub(updates, currentText)

        try:
            with open('README.md', mode='w', encoding='utf8') as f:
                f.write(newText)
                f.close()

            print(updates)
            print('\nUpdates successful!')
        except:
            # Restore original content on failure
            with open('README.md', mode='w', encoding='utf8') as f:
                f.write(currentText)
                f.close()
            raise

    else:
        raise Exception('Badge destination pattern not found in {}'.format(fileName))

def main():
    try:
        # Check provided arguments
        if len(argv) != 3:
            raise ValueError('Invalid number of arguments provided. Expected: {skillsProfileUrl} {limit}')
        else:
            skillsProfileUrl = argv[1]
            limit = int(argv[2])
            
            if limit <= 0:
                raise ValueError('{limit} must be positive integer.')

        with request.urlopen(skillsProfileUrl) as f:
            timestamp = datetime.now(datetime.timezone.utc)
            contents = f.read()

            soup = BeautifulSoup(contents, 'html.parser')

            badges = soup.find('div', attrs={'class': 'profile-badges'})
            print('{} potential badge(s) found.'.format(len(badges)))

            badge_data = dict()

            for badgeEl in badges:
                badge = badgeEl.findNext('span')
                badgeName = badge.text.strip('\r\n')
                badgeName = re.sub('\\s\\s+' , ' ', badgeName)

                if badgeName != '':
                    completion = badge.find_next_sibling().text.strip('\r\n')
                    completion = re.sub('\\s\\s+' , ' ', completion)

                    # Add styling to badge thumbnail
                    thumbnail = badgeEl.findNext('a')
                    thumbnail.find('img').attrs['title'] = completion              
                    thumbnail.find('img').attrs['width'] = '25%'
                    thumbnail.setText(re.sub('\\n\\n+', '', thumbnail.text))

                    badge_data[badgeName] = [thumbnail, completion]

                if len(badge_data) >= limit:
                    break

            badgeCount = len(badge_data)

            if badgeCount > 0:
                if badgeCount < limit:
                    limit = badgeCount

                print('{} badge(s) will be printed.\n'.format(limit))

                generate_readme_text(badge_data, limit, timestamp)

    except Exception as e:
        print("An error occurred: ", e)
        raise e

if __name__ == "__main__":
    main()