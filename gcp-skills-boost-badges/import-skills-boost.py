from datetime import datetime, timezone
from sys import argv
from bs4 import BeautifulSoup
import os.path as path
import re
from urllib import request

def generate_readme_text(badges: dict, skillsProfileUrl: str, fileName: str, numBadges: int, timestamp: datetime):
    """Replaces placeholder in target file with HTML for imported badges

    Args:
        badges (dict): Imported badges from Google Cloud Skills Boost
        skillsProfileUrl (str): URL of a public Google Skills Boost profile
        numBadges (int): Number of badges to output
        timestamp (datetime): Timestamp of badges import

    Raises:
        Exception: Error during file write or placeholder pattern not found
    """
    updates = '<!-- start latest badges --><hr />\n'    
    updates += '### **&#127882; {} Latest Badges from Google Cloud Skills Boost &#127882;**'.format(numBadges)
    updates += '\n_Last checked: {}_'.format(timestamp.isoformat(' ', 'seconds'))
    updates += '\n\n'

    count = 1
    for badgeKey in badges.keys():
        completion = badges[badgeKey][1]

        # Remove extra new lines in <a>
        badgeHtml = ''.join(re.split(r'[\n\t]+', str(badges[badgeKey][0])))
        column = '{}&emsp;&emsp;&emsp;'.format(badgeHtml)

        print('Badge #{} found => {}, {}\n'.format(count, badgeKey, completion))

        updates += column
        count += 1

    updates += '\n\n'
    updates += '#### &#10024; Visit full profile [here]({}) &#10024;'.format(skillsProfileUrl)
    updates += '<hr /><!-- end latest badges -->'

    # Rewrite README with new post content
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
    """Imports badges from a provided Google Cloud Skills public profile into target file

    Raises:
        ValueError: Invalid number of arguments provided. This method expects: {skillsProfileUrl} {targetFile} {numBadges}
        FileNotFoundError: {targetFile} must be valid file in directory
        ValueError: {numBadges} must be greater than 0
        Exception: Error during generate_readme_text(), or other
    """
    try:
        # Check provided arguments
        if len(argv) != 4:
            raise ValueError('Invalid number of arguments provided. Expected: {skillsProfileUrl} {targetFile} {numBadges}')
        else:
            skillsProfileUrl = argv[1]
            fileName = argv[2]
            numBadges = int(argv[3])

            if path.exists(fileName) == False:
                raise FileNotFoundError('{{targetFile}} must be a valid file. (Provided: \'{}\')'.format(fileName))

            if numBadges <= 0:
                raise ValueError('{numBadges} must be positive integer.')

        with request.urlopen(skillsProfileUrl) as f:
            timestamp = datetime.now(timezone.utc)
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
                    img = thumbnail.find('img')

                    img.attrs['title'] = completion              
                    img.attrs['width'] = '25%'

                    badge_data[badgeName] = [thumbnail, completion]

                if len(badge_data) >= numBadges:
                    break

            badgeCount = len(badge_data)

            if badgeCount > 0:
                if badgeCount < numBadges:
                    numBadges = badgeCount

                print('{} badge(s) will be printed.\n'.format(numBadges))

                generate_readme_text(badge_data, skillsProfileUrl, fileName, numBadges, timestamp)

    except Exception as e:
        print("An error occurred:", e)
        raise

if __name__ == '__main__':
    main()
