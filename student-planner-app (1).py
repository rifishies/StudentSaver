import datetime
import json

class Event:
    def __init__(self, name, date, time, division):
        self.name = name
        self.date = date
        self.time = time
        self.division = division

    def to_dict(self):
        return {
            "name": self.name,
            "date": self.date,
            "time": self.time,
            "division": self.division
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["date"], data["time"], data["division"])

class StudentPlanner:
    def __init__(self):
        self.name = ""
        self.divisions = []
        self.events = []
        self.filename = "planner_data.json"

    def setup(self):
        if self.load_data():
            print(f"Welcome back, {self.name}!")
        else:
            self.name = input("Enter your name: ")
            self.setup_divisions()
            print(f"Welcome, {self.name}! Your planner is set up with the following divisions: {', '.join(self.divisions)}")
        self.save_data()

    def setup_divisions(self):
        while True:
            try:
                num_divisions = int(input("How many initial divisions would you like to create? "))
                if num_divisions < 1:
                    print("Please enter a positive number.")
                    continue
                break
            except ValueError:
                print("Please enter a valid number.")

        for i in range(num_divisions):
            while True:
                division = input(f"Enter name for division {i+1}: ").strip()
                if division:
                    self.divisions.append(division)
                    break
                else:
                    print("Division name cannot be empty. Please try again.")

    def add_event(self):
        name = input("Enter event name: ")
        date = input("Enter date (YYYY-MM-DD): ")
        time = input("Enter time (HH:MM): ")
        print("Available divisions:")
        for i, division in enumerate(self.divisions):
            print(f"{i + 1}. {division}")
        division_index = int(input("Enter division number: ")) - 1
        division = self.divisions[division_index]
        event = Event(name, date, time, division)
        self.events.append(event)
        print("Event added successfully!")
        self.save_data()

    def delete_event(self):
        self.view_events()
        if not self.events:
            return
        index = int(input("Enter the number of the event to delete: ")) - 1
        if 0 <= index < len(self.events):
            del self.events[index]
            print("Event deleted successfully!")
            self.save_data()
        else:
            print("Invalid event number.")

    def add_division(self):
        division = input("Enter new division name: ")
        self.divisions.append(division)
        print(f"Division '{division}' added successfully!")
        self.save_data()

    def delete_division(self):
        print("Available divisions:")
        for i, division in enumerate(self.divisions):
            print(f"{i + 1}. {division}")
        index = int(input("Enter the number of the division to delete: ")) - 1
        if 0 <= index < len(self.divisions):
            deleted_division = self.divisions.pop(index)
            self.events = [event for event in self.events if event.division != deleted_division]
            print(f"Division '{deleted_division}' and all associated events deleted successfully!")
            self.save_data()
        else:
            print("Invalid division number.")

    def view_events(self):
        if not self.events:
            print("No events found.")
            return

        view_type = input("View by (1) Whole schedule or (2) Section? ")
        if view_type == "1":
            self.view_whole_schedule()
        elif view_type == "2":
            self.view_by_section()
        else:
            print("Invalid option.")

    def view_whole_schedule(self):
        sorted_events = sorted(self.events, key=lambda e: (e.date, e.time))
        for i, event in enumerate(sorted_events):
            print(f"{i + 1}. {event.date} {event.time} - {event.name} ({event.division})")

    def view_by_section(self):
        order = input("Order by (1) Chronological or (2) Alphabetical? ")
        for division in self.divisions:
            print(f"\n{division}:")
            division_events = [event for event in self.events if event.division == division]
            if order == "1":
                sorted_events = sorted(division_events, key=lambda e: (e.date, e.time))
            elif order == "2":
                sorted_events = sorted(division_events, key=lambda e: e.name.lower())
            else:
                print("Invalid option.")
                return
            for event in sorted_events:
                print(f"  {event.date} {event.time} - {event.name}")

    def save_data(self):
        data = {
            "name": self.name,
            "divisions": self.divisions,
            "events": [event.to_dict() for event in self.events]
        }
        with open(self.filename, "w") as f:
            json.dump(data, f)
        print("Data saved successfully!")

    def load_data(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
            self.name = data["name"]
            self.divisions = data["divisions"]
            self.events = [Event.from_dict(event_data) for event_data in data["events"]]
            return True
        except FileNotFoundError:
            return False

    def run(self):
        self.setup()
        while True:
            print("\nMain Menu:")
            print("1. Add event")
            print("2. Delete event")
            print("3. Add division")
            print("4. Delete division")
            print("5. View schedule")
            print("6. Save and exit")
            choice = input("Enter your choice (1-6): ")

            if choice == "1":
                self.add_event()
            elif choice == "2":
                self.delete_event()
            elif choice == "3":
                self.add_division()
            elif choice == "4":
                self.delete_division()
            elif choice == "5":
                self.view_events()
            elif choice == "6":
                self.save_data()
                print("Thank you for using the Student Planner. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    planner = StudentPlanner()
    planner.run()
