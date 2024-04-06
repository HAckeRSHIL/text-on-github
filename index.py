import sys
import subprocess
from common import charMatrix
from  dating import sunday_at_start
from datetime import datetime, timedelta

skipWeeksFromFront = 2
skipDaysFromAbove = 1
commitPerDayForHighlighed = 5
commitPerDayForShadow = 1

def get_text_input():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return input("Enter the text string: ")



def contruct_printing_matrix(text_input):
    m,n = len(charMatrix['a']), len(charMatrix['a'][0])

    spaceBetweenChars = 2

    printingMatrix = [[] for i in range(m)]
    

    for ch in text_input:
        charMatrixForCh = charMatrix.get(ch, charMatrix['?'])
        for i in range(m):
            printingMatrix[i].extend(charMatrixForCh[i])
        for i in range(spaceBetweenChars):
            for j in range(m):
                printingMatrix[j].append(' ')

    for i in range(m):
        print(''.join(printingMatrix[i]))

    return printingMatrix

def get_commit_dates(printingMatrix,start_date):
    commitDates = []
    
    for j in range(len(printingMatrix[0])):
        referenceDate = start_date + timedelta(days=skipDaysFromAbove)
        for i in range(len(printingMatrix)):
            if printingMatrix[i][j] == '*':
                commitDates.append(referenceDate)
            referenceDate += timedelta(days=1)
        start_date+= timedelta(weeks=1)
    return commitDates

def run_git_command(cmd):
    result = subprocess.run(cmd, shell=True, check=True, text=True)
    return result

def do_the_commits(commitDates,commitPerDay=1):
    for commitDate in commitDates:
        for i in range(commitPerDay):
            formatted_date = commitDate.strftime("%a %b %d %H:%M %Y %z")
            formatted_date_with_timezone = formatted_date + " +0700"
            print(formatted_date_with_timezone)
            cmd = f'GIT_COMMITTER_DATE="{formatted_date_with_timezone}" GIT_AUTHOR_DATE="{formatted_date_with_timezone}" git commit --allow-empty -m "committing on {formatted_date_with_timezone}"'
            run_git_command(cmd)

    cmd = 'git push origin main'
    run_git_command(cmd)


def run_command(command):
    try:
        subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, universal_newlines=True)
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e.output}")
        raise

def cleanup_repo(new_branch_name='temp-branch', commit_message='Initial commit', force_push=False):
    """
     Args:
    - new_branch_name: The name of the temporary orphan branch.
    - commit_message: The commit message for the initial commit.
    - force_push: Whether to force push the changes to the remote repository.
    """
    run_command(f'git checkout --orphan {new_branch_name}')
    run_command('git add .')    
    run_command(f'git commit -m "{commit_message}"')
    
    if force_push:
        main_branch = 'main'  # Change this if your main branch is named differently
        run_command(f'git branch -M {new_branch_name} {main_branch}')
        run_command(f'git push -f origin {main_branch}')




if __name__ == '__main__':
    cleanup_repo(force_push=True)
    commitDates = []
    # text_input = get_text_input().lower()
    
    # printingMatrix = contruct_printing_matrix(text_input)
    # commitDatesDark = get_commit_dates(printingMatrix,sunday_at_start + timedelta(weeks=skipWeeksFromFront))
    # commitDatesShadow = get_commit_dates(printingMatrix,sunday_at_start + timedelta(weeks=skipWeeksFromFront-1))
    # do_the_commits(commitDatesDark,commitPerDayForHighlighed)
    # do_the_commits(commitDatesShadow,commitPerDayForShadow)
    
    
    



