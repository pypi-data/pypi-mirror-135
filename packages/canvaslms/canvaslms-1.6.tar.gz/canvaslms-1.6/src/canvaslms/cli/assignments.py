import canvaslms.cli.courses as courses
import canvaslms.hacks.canvasapi
import csv
import pydoc
import pypandoc
import re
import sys

def assignments_command(config, canvas, args):
  output = csv.writer(sys.stdout, delimiter=args.delimiter)
  course_list = courses.process_course_option(canvas, args)

  for course in course_list:
    if args.ungraded:
      all_assignments = list(list_ungraded_assignments([course]))
    else:
      all_assignments = list(list_assignments([course]))

    assignment_groups = filter_assignment_groups(course, args.regex)

    for assignment_group in assignment_groups:
      assignments = filter_assignments_by_group(
          assignment_group, all_assignments)

      for assignment in assignments:
        output.writerow([assignment_group.name, assignment.name])
def filter_assignment_groups(course, regex):
  """Returns all assignment groups of course whose name matches regex"""
  name = re.compile(regex)
  return filter(
    lambda group: name.search(group.name),
    course.get_assignment_groups())
def filter_assignments_by_group(assignment_group, assignments):
  """Returns elements in assignments that are part of assignment_group"""
  return filter(
      lambda assignment: assignment.assignment_group_id == assignment_group.id,
      assignments)
def assignment_command(config, canvas, args):
  assignment_list = process_assignment_option(canvas, args)
  for assignment in assignment_list:
    pydoc.pager(format_assignment(assignment))
def add_assignment_option(parser):
  try:
    courses.add_course_option(parser)
  except argparse.ArgumentError:
    pass

  parser.add_argument("-a", "--assignment",
    required=False, default=".*",
    help="Regex matching assignment title or Canvas identifier, "
      "default: '.*'")

def process_assignment_option(canvas, args):
  course_list = courses.process_course_option(canvas, args)
  assignments_list = filter_assignments(course_list, args.assignment)
  return list(assignments_list)
def format_assignment(assignment):
  """Returns an assignment formatted for the terminal"""
  instruction = pypandoc.convert_text(
    assignment.description, "md", format="html")

  return f"""# {assignment.name}

{instruction}

URL: {assignment.html_url}
Submissions: {assignment.submissions_download_url}"""
def list_assignments(courses):
  for course in courses:
    for assignment in course.get_assignments():
      assignment.course = course
      yield assignment

def list_ungraded_assignments(courses):
  for course in courses:
    for assignment in course.get_assignments(bucket="ungraded"):
      assignment.course = course
      yield assignment
def filter_assignments(courses, regex):
  """Returns all assignments from courses whose title matches regex"""
  p = re.compile(regex)
  for assignment in list_assignments(courses):
    if p.search(assignment.name):
      yield assignment
    elif p.search(str(assignment.id)):
      yield assignment

def add_command(subp):
  """Adds the subcommands assignments and assignment to argparse parser subp"""
  add_assignments_command(subp)
  add_assignment_command(subp)

def add_assignments_command(subp):
  """Adds the assignments subcommand to argparse parser subp"""
  assignments_parser = subp.add_parser("assignments",
      help="Lists assignments of a course",
      description="Lists assignments of a course. "
        "Output, CSV-format: <Canvas ID> <assignment name>")
  assignments_parser.set_defaults(func=assignments_command)
  courses.add_course_option(assignments_parser)
  assignments_parser.add_argument("regex",
    default=".*", nargs="?",
    help="Regex for filtering assignment groups, default: '.*'")
  assignments_parser.add_argument("-u", "--ungraded", action="store_true",
    help="Show only ungraded assignments.")

def add_assignment_command(subp):
  """Adds the assignment subcommand to argparse parser subp"""
  assignment_parser = subp.add_parser("assignment",
      help="Lists assignment details",
      description="Lists assignment details")
  assignment_parser.set_defaults(func=assignment_command)
  add_assignment_option(assignment_parser)
