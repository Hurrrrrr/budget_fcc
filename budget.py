class Category:

  def __init__(self, name):
    self.name = name
    self.total = 0.0
    self.ledger = []
    self.percentage = 0

  def __repr__(self):
    output = f"{self.name:*^30s}\n"
    for item in self.ledger:
      output += f"{str(item['description'])[:23]:<23s}"
      output += f"{item['amount']:>7.2f}\n"
    output += f"Total: {self.total:.2f}"
    return output

  def deposit(self, amount, description=""):
    self.total += amount
    self.ledger.append({"amount": amount, "description": description})

  def withdraw(self, amount, description=""):
    if not self.check_funds(amount):
      return False
    self.total -= amount
    self.ledger.append({"amount": -amount, "description": description})
    return True

  def get_balance(self):
    return self.total

  def transfer(self, amount, other_category):
    if not self.check_funds(amount):
      return False
    self.withdraw(amount, f"Transfer to {other_category.name}")
    other_category.deposit(amount, f"Transfer from {self.name}")
    return True

  def check_funds(self, amount):
    if amount > self.total:
      return False
    return True


def create_spend_chart(categories):
  label_width = 4
  num_categories = len(categories)

  # calculate category percentages
  grand_total = 0
  for k in range(len(categories)):
    cat_total = 0
    for item in categories[k].ledger:
      if item["amount"] < 0:
        grand_total += abs(item["amount"])
        cat_total += abs(item["amount"])
      categories[k].percentage = cat_total
#     print(f"Cat total: {cat_total:.2f}")
#   print(f"Grand total: {grand_total:.2f}")
  for L in range(len(categories)):
    categories[L].percentage = int(
      (categories[L].percentage / grand_total * 100))
    # print(f"cat percent: {categories[L].percentage}")

  # print graph section
  output = "Percentage spent by category\n"
  for i in range(100, -1, -10):
    output += f"{str(i)+'|':>{label_width}}"
    for j in range(num_categories):
      output += " "
      if categories[j].percentage >= i:
        output += "o"
      else:
        output += " "
      output += " "
    output += "\n"
  output += (" " * label_width) + ("-" * ((3 * num_categories) + 1) + "\n")

  # print names section
  longest = 0
  for cat in categories:
    if len(cat.name) > longest:
      longest = len(cat.name)
  for m in range(longest):
    output += "    "
    for cat in categories:
      output += " "
      try:
        output += cat.name[m]
      except:
        output += " "
      output += " "
    output += "\n"

  return output