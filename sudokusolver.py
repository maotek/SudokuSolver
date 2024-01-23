import tkinter as tk

class sudokusolver(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		Frame(self).pack()

class Frame(tk.Frame):
	def __init__(self,master):
		tk.Frame.__init__(self)
		self.testboard = [
		[8,0,0,0,0,0,0,0,0],
		[0,0,3,6,0,0,0,0,0],
		[0,7,0,0,9,0,2,0,0],
		[0,5,0,0,0,7,0,0,0],
		[0,0,0,0,4,5,7,0,0],
		[0,0,0,1,0,0,0,3,0],
		[0,0,1,0,0,0,0,6,8],
		[0,0,8,5,0,0,0,1,0],
		[0,9,0,0,0,0,4,0,0]
		]
		self.board = [
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0]
		]
		self.aboutboard = [
		['M','A','O','T','E','K',0,0,0],
		['C','O','P','Y','R','I','G','H','T'],
		['2','0','2','1',0,0,0,0,0],
		['S','U','D','O','K','U',0,0,0],
		['S','O','L','V','E','R',0,0,0],
		['V','1.','0',0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0]
		]
		self.d = {k:tk.StringVar() for k in range(1,82)}
		self.e = {e:tk.Entry(self) for e in range(1,82)}

		number = 1

		for j in range(1,12):
			if (j!=4) and (j!=8):
				for i in range(1,12):
					if (i != 4) and (i != 8):
						#self.entry_number = tk.Entry(self,textvariable=self.d[box_number],font='Arial 20',width=2)
						self.e[number].config(textvariable=self.d[number],font='Arial 20',width=2)
						self.e[number].grid(row=j,column=1+i,ipadx=5,ipady=5)
						number += 1
					else:
						label = tk.Label(self,text=' ',font='Arial 5').grid(row=j,column=1+i)
			else:
				label = tk.Label(self,text='',font='Arial 5').grid(row=j,columnspan=20)

		self.button = tk.Button(self,text='Solve',command= lambda: self.finalsolve(),relief='groove').grid(row=13,column=1,columnspan=4,sticky='nesw',ipady=10,pady=6)
		self.button = tk.Button(self,text='Reset',command= lambda: self.reset(),relief='groove').grid(row=13,column=7,sticky='nesw',ipady=10,pady=6)
		self.button = tk.Button(self,text='Test',command= lambda: self.insert(board=self.testboard,reset=True),relief='groove').grid(row=13,column=6,sticky='nesw',ipady=10,pady=6)
		self.button = tk.Button(self,text='About',command= lambda: self.insert(board=self.aboutboard,reset=True,state=False),relief='groove').grid(row=13,column=8,sticky='nesw',ipady=10,pady=6)
		self.response = tk.StringVar()
		self.responselabel = tk.Label(self,textvariable=self.response,font='Arial 10',height=1)
		self.responselabel.grid(row=13,column=10,columnspan=3,sticky='nesw',ipady=10,pady=6)
		self.response.set('MaoTek Sudoku\nSolver')

		self.ok = True
		self.counter = 1

	def reset(self):
		self.board = [
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0]
		]
		self.ok = True
		self.responselabel.config(fg='black')
		self.response.set('MaoTek Sudoku\nSolver')
		for i in range(1,82):
			self.d[i].set('')
			self.e[i].config(state='normal')

	def check(self,rij,column,getal): #returns if number can be placed.
		if self.board[rij][column] == 0 and getal not in self.board[rij]: #check if spot is empty and if the number is not in de row.
			for i in self.board: #check if the number is not in the column.
				if i[column] == getal:
					return False
			else: #check if the number exists in his 3x3 box.	
				rij_ = (rij//3)*3
				
				column_ = (column//3)*3

				if getal in self.board[rij_][column_:column_+3]+self.board[rij_+1][column_:column_+3]+self.board[rij_+2][column_:column_+3]:
					return False
				else:
					return True
		else:
			return False

	def solve(self): #solve sudoku with recursion.
		for i in range(9):
			for j in range(9):
				if self.board[i][j] == 0:
					for k in range(1,10):
						if self.check(i,j,k) and self.ok:
								self.board[i][j] = k
								self.solve()
								self.board[i][j] = 0
					return
		self.ok = False
		#for i in self.board:
			#print(i)
		#print('\n')
		self.insert(board=self.board,state=False)

	def error(self): #raise error
		self.responselabel.config(fg='red')
		self.response.set('ERROR')

	def read(self): #read the board, (this function is called in the pre-check function).
		counter = 1
		for i in range(9):
			for j in range(9):
				if self.d[counter].get() != '':
					self.board[i][j] = int(self.d[counter].get())
				else:
					self.board[i][j] = 0
				counter += 1

	def finalsolve(self):
		try:
			if self.precheck():
				self.solve()
			if self.ok:
				self.responselabel.config(fg='red')
				self.response.set('NO SOLUTION\nPOSSIBLE')
			else:
				self.responselabel.config(fg='green')
				self.response.set('SOLUTION\nFOUND')
		except:
			self.error()

	def insert(self,board,reset=False,state=True):
		if reset:
			self.reset()
		counter = 1
		for i in range(9):
			for j in range(9):
				if board[i][j] != 0:
					self.d[counter].set(board[i][j])
				else:
					self.d[counter].set('')
				counter += 1
		if not state:
			for i in range(1,82):
				self.e[i].config(state='disabled')

	def precheck(self): #check if it can be solved, if not raise error
		self.read()
		for i in self.board:
			l = [x for x in i if x != 0]
			if len(l) != len(set(l)):
				self.error()
				return False
		for i in range(9):
			l = []
			for j in range(9):
				if self.board[j][i] < 10:
					l.append(self.board[j][i])
				else:
					self.error()
					return False
			l_ = [x for x in l if x!= 0]
			if len(l_) != len(set(l_)):
				self.error()
				return False
		for i in range(0,9,3):
			for j in range(0,9,3):
				l = self.board[i][j:j+3]+self.board[i+1][j:j+3]+self.board[i+2][j:j+3]
				l_ = [x for x in l if x!=0]
				if len(l_) != len(set(l_)):
					self.error()
					return False
		return True

if __name__ == '__main__':
	root = sudokusolver()
	root.geometry('430x500')
	root.title('MaoTek Sudoku Solver')
	root.resizable(False,False)
	root.iconbitmap('logo.ico')
	root.mainloop()