import re 

class Item:
	def __init__(self, entry, cost):
		self.entry = entry
		self.cost = cost
	
	def __repr__(self):
		return 'Item(entry: %s, cost: %s)' % (self.entry, self.cost)


class Receipt:
	def __init__(self, receipt_file):
		self.items = []
		self.subtotal = None
		self.tax = None
		self.total = None

	def __repr__(self):
		return 'Data(Items: %s, Tax: %s, Total: %s)' % (self.items, self.tax, self.total)

	def convert_file_to_data(self, receipt_file):
		with open (receipt_file, "r") as text:
			data = text.readlines()
		data_no_spaces = [line.replace('\n', '') for line in data]
		filtered_data = [line for line in data_no_spaces if line.strip()]
		transaction_data = [line for line in filtered_data if line.find('$') != -1]
		return transaction_data

	def make_items(self, data):
		index = 0
		while len(data) > index and "Total" not in data[index]:
			name_entry = data[index].split(re.search('[0-9]', data[index]).group())[0]
			num_entry = int(re.search('[0-9]', data[index]).group())
			cost_entry = float(re.findall(r'\$(.*) ', data[index])[0])
			for count in range(num_entry):
				self.items.append(Item(name_entry, cost_entry))
			index += 1

	def update_total(self, data):
		for line in data:
			if "Sub Total" in line:
				self.subtotal = float(re.findall(r'\$(.*)', line)[0])
			if "Tax" in line:
				self.tax = float(re.findall(r'\$(.*)', line)[0])
			if "Total" in line and "Sub Total" not in line: 
				self.total = float(re.findall(r'\$(.*)', line)[0])

	def get_items(self):
		return self.items

	def get_tax(self):
		return self.tax

	def get_total(self):
		return self.total


vapiano = Receipt("example_receipt.txt")
data = vapiano.convert_file_to_data("example_receipt.txt")
vapiano.make_items(data)
vapiano.update_total(data)
print(vapiano)
