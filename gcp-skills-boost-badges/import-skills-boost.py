from sys import argv
import sys
from bs4 import BeautifulSoup
import re
from urllib import request

skillsProfileUrl = ''
limit = 3

def generate_readme_text(badges: dict, limit = 3):
    updates = '<!-- start latest badges --><hr />\n'
    updates += '### **&#127882; {} Latest Badges from Google Cloud Skills Boost &#127882;**'.format(limit)
    updates += '\n<ol>'

    if len(badges) < limit or limit <= 0:
        limit = len(badges)

    count = 1
    for badgeKey in badges.keys():
        completion = badges[badgeKey][1]
        row = '<li>' + completion + '<br /><br />'
        row += '{}</li><br />'.format(badges[badgeKey][0])

        print('Badge #{} found => {}, {}\n'.format(count, badgeKey, completion))

        updates += row
        count += 1

        if count > limit:
            break

    updates += '</ol>\n\n'
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

        with request.urlopen(skillsProfileUrl) as f:
            contents = f.read()

            soup = BeautifulSoup(contents, 'html.parser')

            badges = soup.find('div', attrs={'class': 'profile-badges'})

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
                    thumbnail.find('img').attrs['width'] = '25%'

                    badge_data[badgeName] = [thumbnail, completion]

            badgeCount = len(badge_data)
            print('{} badge(s) found.'.format(badgeCount))

            if badgeCount > 0:
                print('Up to {} badge(s) will be printed.\n'.format(limit))

                generate_readme_text(badge_data, limit)

    except Exception as e:
        print("An error occurred: ", e)
        sys.exit(1)

if __name__ == "__main__":
    main()