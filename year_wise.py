import requests
from yaspin import yaspin
from rich.console import Console
from rich.table import Table

print(
    "Note: Archive list of GSoC website doesn't render pages using JSON. I had to manually fetch organisation links and then again fetch language stack from each org link. So, this will take some time to fetch everything"
)
archive_url = "https://summerofcode.withgoogle.com/archive/2020/organizations/"
year = int(input("Which year in 2016-2020? "))

archive_url = (
    "https://summerofcode.withgoogle.com/archive/" + str(year) + "/organizations/"
)
language = str(input("Enter language you want to filter out: "))
from bs4 import BeautifulSoup


class Organization:
    def __init__(self, name, irc, org_page, tech_stack):
        self.name = name
        self.irc = irc
        self.org_page = org_page
        self.tech_stack = tech_stack


organization_list = []


def print_list():
    table = Table(title=f"G-soc orgs for {year}")
    table.add_column("S.No", justify="right", style="white")
    table.add_column("Org-name", style="magenta")
    table.add_column("IRC", style="red", width=20)
    table.add_column("Org Link", style="blue", width=20)
    table.add_column("Tech stack", justify="right", style="green")
    index = 1
    for organization in organization_list:
        tech = ""
        for t in organization.tech_stack:
            tech = tech + " " + t
        table.add_row(
            str(index),
            str(organization.name),
            str(organization.irc),
            str(organization.org_page),
            str(tech),
        )
        index += 1
    Console().print(table)
    x = 1
    while x != -1:

        x = int(input("Enter the index no. for getting complete links(-1 to quit): "))
        if x == -1:
            continue
        org_x = organization_list[x - 1]
        try:
            print("Name: " + org_x.name)
            print("IRC: " + org_x.irc)
            print("Organisation Link: " + org_x.org_page)
            print("Tech Stack: " + (" ").join(org_x.tech_stack))
            print("===========================================\n")
        except:
            print("Organisation is missing some value. Kindly check on GSoc Website")


count = 0
try:
    with yaspin(text=f"Loading {year} org ", color="yellow") as spinner:
        # while True:

        response = requests.get(archive_url)
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.find_all("a", {"class": "organization-card__link"}, href=True)
        print(f"There are total {len(links)} organizations. Filtering {language}")
        for link in links:
            org_url = archive_url + (link["href"][28:])
            response_org = requests.get(org_url)
            org_soup = BeautifulSoup(response_org.content, "html.parser")
            org_title = org_soup.find("h3", {"class": "banner__title"}).text
            print(f"#{count} {org_title}")
            count = count + 1
            tech_stack = []
            tech = org_soup.find_all("li", {"class": "organization__tag--technology"})
            for t in tech:
                tech_stack.append(t.text)
            org_irc = org_soup.find(
                "md-button", {"class": "org__meta-button"}, href=True
            )["href"]
            if language in tech_stack:
                current_org = Organization(org_title, org_irc, org_url, tech_stack)
                organization_list.append(current_org)

    spinner.ok("✅ ")
    print_list()
    quit()
except Exception as e:
    print(e)
