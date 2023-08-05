import canvaslms.cli.assignments as assignments
import canvaslms.cli.users as users
import canvaslms.hacks.canvasapi

import argparse
import csv
import pydoc
import pypandoc
import re
import sys
import urllib.request

def submissions_command(config, canvas, args):
  assignment_list = assignments.process_assignment_option(canvas, args)
  if args.ungraded:
    submissions = list_ungraded_submissions(assignment_list)
  else:
    submissions = list_submissions(assignment_list)

  if args.user or args.category or args.group:
    user_list = users.process_user_or_group_option(canvas, args)
    submissions = filter_submissions(submissions, user_list)

  output = csv.writer(sys.stdout, delimiter=args.delimiter)

  for submission in submissions:
    output.writerow(format_submission_short(submission))
def speedgrader(submission):
  """Returns the SpeedGrader URL of the submission"""
  speedgrader_url = submission.preview_url

  speedgrader_url = re.sub("assignments/",
    "gradebook/speed_grader?assignment_id=",
    speedgrader_url)

  speedgrader_url = re.sub("/submissions/",
    "&student_id=",
    speedgrader_url)

  speedgrader_url = re.sub(r"\?preview.*$", "", speedgrader_url)

  return speedgrader_url
def submission_command(config, canvas, args):
  submission_list = process_submission_options(canvas, args)
  for submission in submission_list:
    pydoc.pager(format_submission(submission, canvas))
def add_submission_options(parser):
  try:
    assignments.add_assignment_option(parser)
  except argparse.ArgumentError:
    pass

  try:
    users.add_user_or_group_option(parser)
  except argparse.ArgumentError:
    pass

def process_submission_options(canvas, args):
  assignment_list = assignments.process_assignment_option(canvas, args)
  user_list = users.process_user_or_group_option(canvas, args)
  return list(filter_submissions(list_submissions(assignment_list), user_list))
def list_submissions(assignments, include=["submission_comments"]):
  for assignment in assignments:
    submissions = assignment.get_submissions(include=include)
    for submission in submissions:
      submission.assignment = assignment
      yield submission

def list_ungraded_submissions(assignments, include=["submisson_comments"]):
  for assignment in assignments:
    submissions = assignment.get_submissions(bucket="ungraded",
      include=include)
    for submission in submissions:
      if submission.submitted_at and (submission.graded_at is None or
          not submission.grade_matches_current_submission):
        submission.assignment = assignment
        yield submission
def filter_submissions(submission_list, user_list):
  user_list = set(user_list)

  for submission in submission_list:
    for user in user_list:
      if submission.user_id == user.id:
        submission.user = user
        yield submission
        break
def format_submission_short(submission):
  if submission.submitted_at:
    date = submission.submitted_at
  else:
    date = submission.graded_at
  return [submission.assignment.course.course_code, submission.assignment.name,
    submission.user_id, submission.user.name, submission.grade, date]
def format_submission(submission, canvas):
  """Formats submission for printing to stdout"""
  student = submission.assignment.course.get_user(submission.user_id)

  formatted_submission = f"""# Metadata

{submission.assignment.course.course_code} > {submission.assignment.name}

- Student: {student.name} ({student.login_id or None}, {submission.user_id})
- Submission ID: {submission.id}
- Submitted (graded): {submission.submitted_at} ({submission.graded_at})
- Grade: {submission.grade} ({submission.score})
- SpeedGrader: {speedgrader(submission)}
"""

  try:
    if submission.submission_comments:
      formatted_submission += f"""

# Comments
"""

    for comment in submission.submission_comments:
      formatted_submission += f"""
{comment["author_name"]} ({comment["created_at"]}):

{comment["comment"]}
"""
  except AttributeError:
    pass

  formatted_submission += f"""

# Body

{submission.body}
"""

  try:
    for attachment in submission.attachments:
      if "text/" not in attachment["content-type"]:
        continue

      contents = urllib.request.urlopen(attachment["url"]).read().decode("utf-8")
      formatted_submission += f"""

## {attachment["filename"]}

```
{contents}
```
"""
  except AttributeError:
    pass

  return formatted_submission

def add_command(subp):
  """Adds the submissions and submission commands to argparse parser subp"""
  add_submissions_command(subp)
  add_submission_command(subp)

def add_submissions_command(subp):
  """Adds submissions command to argparse parser subp"""
  submissions_parser = subp.add_parser("submissions",
      help="Lists submissions of an assignment",
      description="Lists submissions of assignment(s). Output format: "
        "<Canvas-user-ID> <grade> <grade date>")
  submissions_parser.set_defaults(func=submissions_command)
  assignments.add_assignment_option(submissions_parser)
  users.add_user_or_group_option(submissions_parser)
  submissions_parser.add_argument("-U", "--ungraded", action="store_true",
    help="Show only ungraded submissions.")

def add_submission_command(subp):
  """Adds submission command to argparse parser subp"""
  submission_parser = subp.add_parser("submission",
    help="Prints information about a submission",
    description="Prints data about matching submissions, "
      "including submission and grading time, any text-based attachments.")
  submission_parser.set_defaults(func=submission_command)
  add_submission_options(submission_parser)
