from auth import register_user, login_user, reset_password
from learning import learning_menu
from quiz_engine import start_full_mock, smart_revision


# =========================
# 🚀 MAIN APP
# =========================
def main():

    current_user = None  # SESSION TRACKING

    while True:
        print("\n===== 🧠 UPSC InsightX =====")
        print("1. Register")
        print("2. Login")
        print("3. Reset Password")
        print("4. Learn (NCERT)")
        print("5. Start Full Test")
        print("6. Exit")

        choice = input("Enter your choice: ")

        # =========================
        # REGISTER
        # =========================
        if choice == "1":
            register_user()

        # =========================
        # LOGIN
        # =========================
        elif choice == "2":
            user = login_user()
            if user:
                current_user = user
                user_dashboard(current_user)

        # =========================
        # RESET PASSWORD
        # =========================
        elif choice == "3":
            reset_password()

        # =========================
        # LEARNING (OPTIONAL LOGIN)
        # =========================
        elif choice == "4":
            if current_user:
                learning_menu(current_user)
            else:
                print("⚠️ Please login to track progress!")

        # =========================
        # FULL MOCK TEST
        # =========================
        elif choice == "5":
            if current_user:
                start_full_mock(current_user)
            else:
                print("⚠️ Please login first!")

        # =========================
        # EXIT
        # =========================
        elif choice == "6":
            print("👋 Exiting UPSC InsightX. Goodbye!")
            break

        else:
            print("❌ Invalid choice!")


# =========================
# 👤 USER DASHBOARD
# =========================
def user_dashboard(username):

    while True:
        print(f"\n===== Welcome {username} =====")
        print("1. Learn (NCERT)")
        print("2. Start Full Test")
        print("3. Smart Revision 🧠")
        print("4. Logout")

        choice = input("Choose option: ")

        if choice == "1":
            learning_menu(username)

        elif choice == "2":
            start_full_mock(username)

        elif choice == "3":
            smart_revision(username)

        elif choice == "4":
            print(f"👋 Logging out {username}...")
            break

        else:
            print("❌ Invalid choice!")


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    main()