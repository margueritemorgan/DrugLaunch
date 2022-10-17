# import necessary libraries
import random
import time

class Drug:

    """Class that builds Drug profile using player input and random assignment"""

    def __init__(self):

        # create list of possible therapeutic areas player can choose from
        ta_list = ["breast cancer", "acute leukemia", "chronic leukemia"]

        # ask player to choose a therapeutic area and a name for their drug
        while True:
            self.ta = str(input("\nPlease choose from the following therapeutic areas to launch your drug in: \n \n"
            "Breast Cancer \n"
            "Acute Leukemia \n"
            "Chronic Leukemia \n \n"))
            self.ta = self.ta.lower()
            if self.ta in ta_list:
                break
            else:
                print("Please ensure you've typed the therapeutic area correctly.")

        self.name = str(input("Please choose a name for your drug: \n"))
        self.name = self.name.capitalize()

        # randomly assign other elements of drug profile
        self.lot = random.choice(["front line", "relapsed & refractory"])
        self.duration = random.choice(["fixed treatment duration", "treat-to-progression"])
        self.clin_ben = random.choice(["slight increase in overall survival", "large increase in overall survival"])
        self.admin = random.choice(["oral", "infusion"])
        self.dose = random.randint(200, 500)
        self.cost_diff = random.randint(-100000, 100000)
        self.medicare_lives = random.randint(0, 100)
        self.commercial_lives = 100-self.medicare_lives

        # create a variable to store whether the cost diff is less or more than the standard of care
        if self.cost_diff <0:
            self.cost_diff_label = "less"
        else:
            self.cost_diff_label = "more"

        # determine eligible patients and number of other treatment options based on therapeutic area and line of therapy
        if self.ta == "breast cancer":
            if self.lot == "front line":
                self.elg_pts = 35000
                self.num_trts = 5
            else:
                self.elg_pts = 40000
                self.num_trts = 7
        if self.ta == "acute leukemia":
            if self.lot == "front line":
                self.elg_pts = 17000
                self.num_trts = 3
            else:
                self.elg_pts = 6000
                self.num_trts = 2
        if self.ta == "chronic leukemia":
            if self.lot == "front line":
                self.elg_pts = 18000
                self.num_trts = 3
            else:
                self.elg_pts = 19000
                self.num_trts = 5

    # create a method to share with the player their drug profile
    def get_profile(self):
        print(f"\n{self.name.capitalize()} Profile: \nTherapeutic Area: {self.ta.capitalize()} \nLine of Therapy: {self.lot}"
             f"\nClinical Benefit: {self.clin_ben} compared to the standard of care \nDuration: {self.duration}"
             f"\nAdministration and Dosage: {self.admin}, {self.dose} mgs daily \nCost: ${abs(self.cost_diff)} {self.cost_diff_label} compared "
             f"to the standard of care \nEligible Patients: {self.elg_pts} eligible patients this year \n"
              f"Number of Other Treatment Options: {self.num_trts} \nPayer Breakdown: {self.medicare_lives}% "
              f"Medicare patients and {self.commercial_lives}% Commercial patients\n")

class Payer:
    """Parent class for all payer negotiations."""

    def __init__(self, payer_clin_ben, payer_duration, payer_cost_diff, payer_elg_pts, payer_num_trts):
        self.payer_clin_ben = payer_clin_ben
        self.payer_duration = payer_duration
        self.payer_cost_diff = payer_cost_diff
        self.payer_elg_pts = payer_elg_pts
        self.payer_num_trts = payer_num_trts
        self.man_score = 0

    # calculate payer management score based on player offered rebate
    def negotiate(self, rebate):
        self.rebate = rebate

        if (self.payer_elg_pts >= 15000) & (self.payer_num_trts > 2):
            if self.payer_clin_ben == 'slight increase in overall survival':
                self.man_score += 2
                if self.payer_duration == 'treat-to-progression':
                    self.man_score += 1
                if self.payer_cost_diff >= 0:
                    self.man_score += 1
            else:
                if self.payer_cost_diff >= 10000:
                    self.man_score += 1
        else:
            if self.payer_cost_diff >= 25000:
                self.man_score += 1

        # factor in rebate to payer manaagement score
        if self.rebate >= 20:
            self.man_score -= 2
        elif (self.rebate >= 5) and (self.rebate < 20):
            self.man_score -= 1

        return self.man_score

class Medicare(Payer):
    """Child class for Medicare payer negotiations"""

    def __init__(self, payer_clin_ben, payer_duration, payer_cost_diff, payer_elg_pts, payer_num_trts, Medicare_rebate):
        super().__init__(payer_clin_ben, payer_duration, payer_cost_diff, payer_elg_pts, payer_num_trts)
        self.leakage = -1
        self.Medicare_rebate = Medicare_rebate
        self.Medicare_manage(self.Medicare_rebate)

    # calculate Medicare management score using leakage factor and player offered rebate
    def Medicare_manage(self, Medicare_neg_rebate):
        self.Medicare_man_score = self.negotiate(Medicare_neg_rebate) + self.leakage
        if self.Medicare_man_score < 0:
            self.Medicare_man_score = 0

    def __repr__(self):
        if self.Medicare_man_score == 0:
            return "Congratulations! Your Medicare management score is " + str(self.Medicare_man_score) + ". \nMedicare will not restrict access for patients."
        elif self.Medicare_man_score == 1:
            return "Your Medicare management score is " + str(self.Medicare_man_score) + ". \nMedicare will require Oncologists to get a prior authorization from them before prescribing your treatment."
        elif self.Medicare_man_score == 2:
            return "Your Medicare management score is " + str(self.Medicare_man_score) + ". \nMedicare will require Oncologists to first receive the standard of care before prescribing your treatment."
        elif self.Medicare_man_score == 3:
            return "Your Medicare management score is " + str(self.Medicare_man_score) + ". \nMedicare will require Oncologists to first receive the standard of care and also seek prior authorization \nfrom them before prescribing your treatment."
        else:
            return "Uh oh... Your Medicare management score is " + str(self.Medicare_man_score) + ". \nMedicare will completely restrict access for patients."

class Commercial(Payer):
    """Child class for Commercial payer negotiations"""

    def __init__(self, payer_clin_ben, payer_duration, payer_cost_diff, payer_elg_pts, payer_num_trts, Commercial_rebate):
        super().__init__(payer_clin_ben, payer_duration, payer_cost_diff, payer_elg_pts, payer_num_trts)
        self.Commercial_rebate = Commercial_rebate
        self.Commercial_manage(self.Commercial_rebate)

    # calculate Commercial management score using player offered rebate
    def Commercial_manage(self, Commercial_neg_rebate):
        self.Commercial_man_score = self.negotiate(Commercial_neg_rebate)
        if self.Commercial_man_score < 0:
            self.Commercial_man_score = 0

    def __repr__(self):
        if self.Commercial_man_score == 0:
            return "Congratulations! Your Commercial management score is " + str(self.Commercial_man_score) + ". \nCommercial payers will not restrict access for patients."
        elif self.Commercial_man_score == 1:
            return "Your Commercial management score is " + str(self.Commercial_man_score) + ". \nCommercial payers will require Oncologists to get a prior authorization from them before prescribing your treatment."
        elif self.Commercial_man_score == 2:
            return "Your Commercial management score is " + str(self.Commercial_man_score) + ". \nCommercial payers will require Oncologists to first receive the standard of care before prescribing your treatment."
        elif self.Commercial_man_score == 3:
            return "Your Commercial management score is " + str(self.Commercial_man_score) + ". \nCommercial payers will require Oncologists to first receive the standard of care and also seek prior authorization \nfrom them before prescribing your treatment."
        else:
            return "Uh oh... Your Commercial management score is " + str(self.Commercial_man_score) + ". \nCommercial payers will completely restrict access for patients."

class Education:
    """Class for educating patients and physicians about the new drug"""

    def __init__(self, edu_admin, edu_duration, edu_elg_pts, edu_num_trts):
        self.edu_admin = edu_admin
        self.edu_duration = edu_duration
        self.edu_elg_pts = edu_elg_pts
        self.edu_num_trts = edu_num_trts
        self.optimal_marketing_spend_dict = {"Sales Force" : 0, "Digital Patient Campaign" : 0, "Oncologist Email Campaign" : 0}
        self.optimal_marketing_plan()

    # determine optimal marketing mix plan
    def optimal_marketing_plan(self):
        if (self.edu_elg_pts >= 20000) & (self.edu_num_trts > 3):
            self.optimal_marketing_spend_dict['Sales Force'] = 80
            if self.edu_duration == 'fixed treatment duration':
                self.optimal_marketing_spend_dict['Digital Patient Campaign'] = 15
                self.optimal_marketing_spend_dict['Oncologist Email Campaign'] = 5
            else:
                self.optimal_marketing_spend_dict['Digital Patient Campaign'] = 0
                self.optimal_marketing_spend_dict['Oncologist Email Campaign'] = 20
        else:
            self.optimal_marketing_spend_dict['Sales Force'] = 60
            if self.edu_duration == 'fixed treatment duration':
                self.optimal_marketing_spend_dict['Digital Patient Campaign'] = 30
                self.optimal_marketing_spend_dict['Oncologist Email Campaign'] = 10
            else:
                self.optimal_marketing_spend_dict['Digital Patient Campaign'] = 0
                self.optimal_marketing_spend_dict['Oncologist Email Campaign'] = 40

    # calculate education score based on difference between optimal marketing mix plan and player inputted marketing mix plan
    def calc_education_score(self, player_marketing_spend_dict):
        self.player_marketing_spend_dict = player_marketing_spend_dict
        self.sales_diff = abs(self.optimal_marketing_spend_dict.get('Sales Force') - self.player_marketing_spend_dict.get('Sales Force'))
        self.email_diff = abs(self.optimal_marketing_spend_dict.get('Oncologist Email Campaign') - self.player_marketing_spend_dict.get('Oncologist Email Campaign'))
        self.patient_diff = abs(self.optimal_marketing_spend_dict.get('Digital Patient Campaign') - self.player_marketing_spend_dict.get('Digital Patient Campaign'))
        self.edu_percent_diff = self.sales_diff + self.email_diff + self.patient_diff

        # assign score 0-4 based on difference between optimal and player inputted marketing mix plan
        if self.edu_percent_diff <= 40:
            self.edu_score = 0
        elif 40 < self.edu_percent_diff <= 80:
            self.edu_score = 1
        elif 80 < self.edu_percent_diff <= 120:
            self.edu_score = 2
        elif 120 < self.edu_percent_diff <= 160:
            self.edu_score = 3
        else:
            self.edu_score = 4

        # identify the area of the marketing mix plan the player performed worst on
        self.biggest_diff = max(self.sales_diff, self.email_diff, self.patient_diff)

    def __repr__(self):
        if self.edu_score == 0:
            return "Congratulations! You've created an optimized marketing plan. Your final education score is " + str(self.edu_score) + "."
        elif 1 <= self.edu_score <= 3:
            return "Close! But your marketing plan was not optimized. An ideal marketing plan would be: \n\nSales Force: " + str(self.optimal_marketing_spend_dict.get('Sales Force')) + "\nOncologist Email Campaign: " + str(self.optimal_marketing_spend_dict.get('Oncologist Email Campaign')) + "\nDigital Patient Campaign: " + str(self.optimal_marketing_spend_dict.get('Digital Patient Campaign')) + "\n\nYour final education score is: " + str(self.edu_score)
        else:
            return "Uh oh.. Your marketing plan was far from optimized. An ideal marketing plan would be: \n\nSales Force: " + str(self.optimal_marketing_spend_dict.get('Sales Force')) + "\nOncologist Email Campaign: " + str(self.optimal_marketing_spend_dict.get('Oncologist Email Campaign')) + "\nDigital Patient Campaign: " + str(self.optimal_marketing_spend_dict.get('Digital Patient Campaign')) + "\n\nYour final education score is: " + str(self.edu_score)

class DrugSupply:
    """Class for determining appropriate drug supply"""

    def __init__(self, supply_elg_pts, supply_dosing, supply_duration):
        self.supply_elg_pts = supply_elg_pts
        self.supply_dosing = supply_dosing
        self.supply_duration = supply_duration
        self.necessary_supply()

    # calculate necessary supply
    def necessary_supply(self):
        if self.supply_duration == "fixed treatment duration":
            self.needed_supply = round(((self.supply_dosing * (365/2) * self.supply_elg_pts) +
            ((self.supply_dosing * (365/2) * self.supply_elg_pts)*0.1))/1000000,0)
        else:
            self.needed_supply = round(((self.supply_dosing * 365 * self.supply_elg_pts) +
            ((self.supply_dosing * (365/2) * self.supply_elg_pts)*0.1))/1000000,0)

    def calc_supply_score(self, player_supply_estimate):
        self.percent_diff = round(((self.needed_supply - player_supply_estimate) / self.needed_supply)*100, 0)
        if self.percent_diff > 10:
            self.supply_score = 4
        elif 0 < self.percent_diff <= 10:
            self.supply_score = 3
        elif -10 < self.percent_diff <= 0:
            self.supply_score = 0
        elif -20 < self.percent_diff <= -10:
            self.supply_score = 1
        else:
            self.supply_score = 2

    def __repr__(self):
        if self.supply_score == 0:
            return "Congratulations! You've guess exactly how much drug would be needed! \n\nYour supply score is: " + str(self.supply_score)
        elif (self.supply_score == 1) | (self.supply_score == 2):
            return "You've overestimated the amount of drug needed by " + str(abs(self.percent_diff)) + "%. \n\nYour supply score is: " + str(self.supply_score)
        else:
            return "Uh oh.. You've underestimated the amoung of drug needed by " + str(abs(self.percent_diff)) + "%. \n\nYour supply score is: " + str(self.supply_score)

class Learnings():
    """Class to determine whether player won or lost and share what they should improve on for next time"""
    
    def __init__(self, l_Medicare_man_score, l_Commercial_man_score, l_edu_score, l_supply_score):
        self.l_Medicare_man_score = l_Medicare_man_score
        self.l_Commercial_man_score = l_Commercial_man_score
        self.l_edu_score = l_edu_score
        self.l_supply_score = l_supply_score

    def final_score(self):
        self.total_score = self.l_Medicare_man_score + self.l_Commercial_man_score + self.l_edu_score + self.l_supply_score
        self.worst_score = max(self.l_Medicare_man_score, self.l_Commercial_man_score, self.l_edu_score, self.l_supply_score)
        self.areas_for_improvement = []

        if self.l_Medicare_man_score == self.worst_score:
            self.areas_for_improvement.append("ensuring access for Medicare patients")
        elif self.l_Commercial_man_score == self.worst_score:
            self.areas_for_improvement.append("ensuring access for Commercial patients")
        elif self.l_edu_score == self.worst_score:
            self.areas_for_improvement.append("educating Oncologists on the new treatment option")
        elif self.l_supply_score == self.worst_score:
            self.areas_for_improvement.append("determining the appropriate amount of drug supply")

    def __repr__(self):
        if self.total_score == 0:
            return "Congratulations on successfully launching your drug! Play again soon!"
        else:
            if len(self.areas_for_improvement) > 1:
                for i in self.areas_for_improvement:
                    final_areas += " & ".join(i)
                return "Unfortunately, there were some hiccups in launching your drug. Next time, work on " + final_areas + "."
            else:
                final_area = self.areas_for_improvement[0]
                return "Unfortunately, there were some hiccups in launching your drug. Next time, work on " + final_area + "."

class PlayerNav():

    """Main class that navigates a player through the game."""

    def __init__(self):
        self.drug1 = Drug()

    def enter_drug_prof(self):
        self.drug1.get_profile()

        print("--------------------------------------------------------------------------------------------------------------")

        time.sleep(5)

        self.enter_payer_negotiation(self.drug1.clin_ben, self.drug1.duration, self.drug1.cost_diff, self.drug1.ta,
                                     self.drug1.name, self.drug1.medicare_lives, self.drug1.commercial_lives)

    def enter_payer_negotiation(self, clin_ben, duration, cost_diff, ta, name, medicare_lives, commercial_lives):
        # Print welcome message for payer negotiation phase
        print(f"\nPHASE 1: Negotiating with Payers")
        print(f"\nThe first step in your launch journey is to negotiate with Payers to ensure access to {self.drug1.name} \n"
             f"for {self.drug1.ta.capitalize()} patients. Recall that {self.drug1.medicare_lives}% of patients will likely have insurance \n"
            f"through Medicare and the remaining {self.drug1.commercial_lives}% will likely be Commercially insured patients. \n"
             f"In order to negotiate with payers you can choose to pay a rebate in return for increased access. \n"
              f"Note that Medicare has slightly less ability to implement their management tactics and thus you may have to pay \n"
              f"less rebate for increased access. You only get one chance to negotiate with each payer! \n"
              f"\nLet's first enter into negotiations with Medicare. \n")

        time.sleep(8.00)

        # Calculate Medicare default management
        Medicare_default_management = Medicare(self.drug1.clin_ben, self.drug1.duration, self.drug1.cost_diff, self.drug1.elg_pts, self.drug1.num_trts, 0)
        print(Medicare_default_management)

        # Ask whether player wants to enter into negotiation.
        while True:
            Medicare_rebate = input("What rebate (i.e. percent discount) would you like to pay? Please enter a number 0-100.\n")
            try:
                Medicare_rebate = int(Medicare_rebate)
                if (0 <= Medicare_rebate <= 100):
                    break
                else:
                    print("Please ensure your number is between 0 and 100.\n")
            except ValueError:
                print("Please ensure you've typed a number.\n")

        # Share final Medicare management
        if Medicare_rebate == 0:
            print(f"You have chosen not to negotiate with Medicare.\n")
            self.final_medicare_man_score = Medicare_default_management.Medicare_man_score
        else:
            Medicare_new_management = Medicare(self.drug1.clin_ben, self.drug1.duration, self.drug1.cost_diff, self.drug1.elg_pts, self.drug1.num_trts, Medicare_rebate)
            print(f"After paying a {Medicare_rebate}% rebate, {Medicare_new_management}")
            self.final_medicare_man_score = Medicare_new_management.Medicare_man_score

        # Calculate Commercial default management
        print("Next let's enter into negotiations with Commercial payers.\n")
        time.sleep(5.00)
        Commercial_default_management = Commercial(self.drug1.clin_ben, self.drug1.duration, self.drug1.cost_diff, self.drug1.elg_pts, self.drug1.num_trts, 0)
        print(Commercial_default_management)

        # Ask whether player wants to enter into negotiation.
        while True:
            Commercial_rebate = input("What rebate (i.e. percent discount) would you like to pay? Please enter a number 0-100.\n")
            try:
                Commercial_rebate = int(Commercial_rebate)
                if (0 <= Commercial_rebate <= 100):
                    break
                else:
                    print("Please ensure your number is between 0 and 100.\n")
            except ValueError:
                print("Please ensure you've typed a number.\n")

        # Share final Commercial management
        if Commercial_rebate == 0:
            print(f"You have chosen not to negotiate with Commercial payers.")
            self.final_commercial_man_score = Commercial_default_management.Commercial_man_score
        else:
            Commercial_new_management = Commercial(self.drug1.clin_ben, self.drug1.duration, self.drug1.cost_diff, self.drug1.elg_pts, self.drug1.num_trts, Commercial_rebate)
            print(f"After paying a {Commercial_rebate}% rebate, {Commercial_new_management}")
            self.final_commercial_man_score = Commercial_new_management.Commercial_man_score

        time.sleep(5.0)
        self.enter_education()

    def enter_education(self):
        print("\n--------------------------------------------------------------------------------------------------------------")
        print(f"\nPHASE 2: Educating Oncologists")
        print(f"\nAs the Commercial Lead, you must determine how to distribute your budget across various \n"
                f"marketing tactics in order to educate physicians and patients about {self.drug1.name}. The 3 \n"
                f"marketing tactics at your disposal are: \n1) Sales Force - hire individuals to have in-person conversations "
                f"with Oncologists about {self.drug1.name} \n2) Oncologist Email Campaign - send emails to Oncologists "
                f"with information about {self.drug1.name} \n3) Digital Patient Campaign - share information directly with "
              f"patients about {self.drug1.name}.\n")

        chosen_marketing_spend_dict = {"Sales Force" : 0, "Digital Patient Campaign" : 0, "Oncologist Email Campaign" : 0}
        while True:
            while True:
                chosen_marketing_spend_dict["Sales Force"] = input("What percent of your budget would you like to spend on your Sales Force? Enter a number 0-100.\n")
                try:
                    chosen_marketing_spend_dict["Sales Force"] = int(chosen_marketing_spend_dict["Sales Force"])
                    if (0 <= chosen_marketing_spend_dict.get("Sales Force") <= 100):
                        break
                    else:
                        print("Please ensure your number is between 0 and 100.\n")
                except ValueError:
                    print("Please ensure you've typed a number.\n")
            while True:
                chosen_marketing_spend_dict["Oncologist Email Campaign"] = input("What percent of your budget would you like to spend on your Oncologist Email Campaign? Enter a number 0-100.\n")
                try:
                    chosen_marketing_spend_dict["Oncologist Email Campaign"] = int(chosen_marketing_spend_dict["Oncologist Email Campaign"])
                    if (0 <= chosen_marketing_spend_dict.get("Oncologist Email Campaign") <= 100) & ((chosen_marketing_spend_dict.get("Oncologist Email Campaign") + chosen_marketing_spend_dict.get("Sales Force")) <= 100):
                        break
                    elif chosen_marketing_spend_dict.get("Oncologist Email Campaign") not in range(0,101):
                        print("Please ensure your number is between 0 and 100.\n")
                    elif (chosen_marketing_spend_dict.get("Oncologist Email Campaign") + chosen_marketing_spend_dict.get("Sales Force")) > 100:
                        print("Please ensure your Sales Force and Oncologist Email Campaign budgets aren't more than 100% of your overall budget.\n")
                except ValueError:
                    print("Please ensure you've typed a number.\n")

            chosen_marketing_spend_dict["Digital Patient Campaign"] = 100 - (chosen_marketing_spend_dict.get("Sales Force") + chosen_marketing_spend_dict.get("Oncologist Email Campaign"))
            print(f"\nYour marketing budget is divided as follows: \nSales Force: {chosen_marketing_spend_dict.get('Sales Force')}% \nOncologist Email"
                 f" Campaign: {chosen_marketing_spend_dict.get('Oncologist Email Campaign')}% \nPatient Digital Campaign: {chosen_marketing_spend_dict.get('Digital Patient Campaign')}% \n")

            while True:
                education_exit = str(input("Would you like to continue with your selected budget breakdown? \nEnter 'Yes' to continue or 'No' to redo.\n"))
                education_exit = education_exit.lower()
                if (education_exit == "yes") | (education_exit == "no"):
                    break
                else:
                    print("Please enter Yes or No.")

            if education_exit == "yes":
                break

        ed1 = Education(self.drug1.admin, self.drug1.duration, self.drug1.elg_pts, self.drug1.num_trts)
        ed1.calc_education_score(chosen_marketing_spend_dict)
        print(ed1)
        self.final_edu_score = ed1.edu_score
        time.sleep(5.00)
        self.enter_drug_supply()

    def enter_drug_supply(self):
        print("\n--------------------------------------------------------------------------------------------------------------")
        print(f"\nPHASE 3: Determining Appropriate Drug Supply")
        print(f"\nYour last and final stage in launching {self.drug1.name} is to determine how much drug supply \nwill"
             f" be needed in year 1. Recall that there are {self.drug1.elg_pts} {self.drug1.ta} patients that \n"
             f"will be diagnosed in a given year. These patients will take {self.drug1.dose} mgs per day and their regimen \n"
             f"is {self.drug1.duration}. Assume for now that a fixed treatment duration regimen will last ~6 months \n"
             f"whereas a treat-to-progression regimen will last the full year.\n")

        time.sleep(4)

        while True:
            drug_supply_estimate = float(input("Please enter the amount of drug you plan to supply in year 1. Enter your amount in millions of mgs: "))
            try:
                drug_supply_estimate = int(drug_supply_estimate)
                if drug_supply_estimate >= 0:
                    break
                else:
                    print("Please ensure your number is >= to 0.\n")
            except ValueError:
                print("Please ensure you've entered a number.\n")

        ds1 = DrugSupply(self.drug1.elg_pts, self.drug1.dose, self.drug1.duration)
        ds1.calc_supply_score(drug_supply_estimate)
        print(ds1)
        self.final_supply_score = ds1.supply_score

        time.sleep(3)
        self.enter_learnings()

    def enter_learnings(self):
        print("\n--------------------------------------------------------------------------------------------------------------")
        print(f"\nYou've completed the game.\n")
        l1 = Learnings(self.final_medicare_man_score, self.final_commercial_man_score, self.final_edu_score, self.final_supply_score)
        l1.final_score()
        print(l1)

print("\nWelcome to DrugLaunch! \n")
time.sleep(2.0)
print("You are the Commercial Lead for a pharmaceutical company and are responsible for launching \n"
        "a new Oncology treatment on the US healthcare market. There will be 3 phases of the game \n"
      "to navigate through in order to successfully launch your drug: \n\n1) Negotiating with payers \n2)"
      " Educating Oncologists \n3) Determining the appropriate drug supply")
time.sleep(8.0)
print("\nYou will receive a score for each "
      "phase between 0-4 with 0 being the best and 4 being the worst. Your total score will determine whether you have \nsuccessfully launched the drug or not.")
time.sleep(2.0)
print("\nFirst, let's determine what drug you'd like to launch. Good luck!!")
print("\n--------------------------------------------------------------------------------------------------------------")
time.sleep(4.00)

PlayerNav().enter_drug_prof()
