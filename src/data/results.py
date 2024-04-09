import openpyxl as op

def save_results(cell_id, new_value):
  """
  Saves and updates a cell with the new value in `results.xlsx`
  """
  workbook = op.load_workbook("./src/data/results.xlsx")
  sheet = workbook.worksheets[0]

  sheet[cell_id] = new_value

  workbook.save("./src/data/results.xlsx")