#creating class with their attributes
class Goal:
    def __init__(self, title, description):

        self.title = title

        self.description = description

        self.completed = False

#defining method to mark it complete
    def mark_completed(self):
        self.completed = True

#defining method to return goal info
    def __str__(self):

        status = "Completed" if self.completed else "In progress"

        return f"Goal: {self.title}\nDescription: {self.description}\nStatus: {status}"

#creating goal tracker class with their attributes
    
class GoalTracker:
    # defining method to add new goal
    def __init__(self):
        self.goals = []

    def add_goal(self,title,description):
        new_goal = Goal(title, description)
        self.goals.append(new_goal)

        print ("\nGoal added successfully!")

    #defining method to list goals
    def list_goals(self):
        if not self.goals:
            print("\nNo goals to display")
            return
        print("\nYour Goals:")

        for idx, goal in enumerate(self.goals,1):
            print(f"{idx}. {goal.title} - {'completed' if goal.completed else'In Progess'}")
    
    #defining method to mark it
    def mark_goal_completed(self, index):
        if 0 <= index < len(self.goals):
            self.goals[index].mark_completed()
            print("nGoal marked as completed")
        else:
            print("\nInvalid goal number.")

    #defining method to delete goal
    def delete_goal(self, index):
        if 0 <= index< len(self.goals):
            removed_goal = self.goals.pop(index)
            print(f"\nGoal '{removed_goal.title}' deleted.")
        else:
            print("\nInvalid goal number.")

    #defining method to show goal details
    def show_goals_details(self, index):
        if 0 <= index < len(self.goals):
            print("\n" + str(self.goals[index]))
        else:
            print("\nInvalid goal number.")

 #creating display menu
def display_menu():
    print("\nGoal Tracking App Menu")
    print("1. Add a new goal")
    print("2. List All Goals")
    print("3. Mark Goal as Completed")
    print("4. Delete a Goal")
    print("5. View Goal Details")
    print("6. exit")

#defining function for user interaction
def main():
    tracker = GoalTracker()
    while True:
        display_menu
        choice = input("\nEnter your choice (1-6): ")

        if choice == "1":
            title = input("nEnter goal title: ")
            description = input("Enter goal description: ")
            tracker.add_goal(title, description)

        elif choice == "2":
            tracker.list_goals()

        elif choice == "3":
            tracker.list_goals()
            index = int(input("\nEnter the goal number to mark as completed: ")) -1
            tracker.mark_goal_completed(index)

        elif choice == "4":
            tracker.list_goals()
            index = int(input("\nEnter the goal number to delete: ")) -1
            tracker.delete_goal(index)

        elif choice == "5":
            tracker.list_goals()
            index = int(input("\nEnter the goal number to view details: ")) -1
            tracker.show_goals_details(index)

        elif choice == "6":
            print("nExiting Goal Tracking App. Goobye!")
            break

        else:

            print("\nInvalit choice, please try again.")
## Adding code running script
if __name__ == "__main__":
    main()


