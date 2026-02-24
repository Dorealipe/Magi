import random, math
from os import system
# ===============================================
# === DEFINIÇÕES DE CLASSES AUXILIARES ===
# ===============================================
# --- Classe Posição ---
class Position:
	def __init__(self,x,y):
		self.x = x
		self.y = y
	@property
	def pos(self):
		return Position(self.x, self.y)
	@pos.setter
	def pos(self, value):
		self.x, self.y = value
	def __str__(self):
		return str((self.x,-self.y))
	def __repr__(self):
		return str(self)
	def euclidean_distance(self, other):
		return math.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)
	def manhattan_distance(self, other):
		return abs(self.x - other.x) + abs(self.y - other.y)
	def __eq__(self, value):
		if not isinstance(value, Position):
			return False
		return self.x == value.x and self.y == value.y
	def __iter__(self):
		yield self.x
		yield self.y
	def __add__(self, other):
		return Position(self.x + other.x, self.y + other.y)
	def __sub__(self, other):
		return Position(self.x - other.x, self.y - other.y)
	@staticmethod
	def xy(number):
		return Position(number,number)
	def rotate(self, direction):
		if direction == 'r': # (-1,-1) -> (0,-1) -> (1,-1) -> (1,0) -> (1,1) -> (0,1) -> (-1,1) -> (-1,0)
			return Position(self.x+1, self.y) if self.y == 0 else Position(self.x, self.y-1) if self.x > 0 else Position(self.x-1, self.y) if self.y < 0 else Position(self.x, self.y+1) if self.x < 0 else Position(self.x+1, self.y)
		elif direction == 'l':
			return Position(self.x-1, self.y) if self.y == 0 else Position(self.x, self.y+1) if self.x > 0 else Position(self.x+1, self.y) if self.y < 0 else Position(self.x, self.y-1) if self.x < 0 else Position(self.x-1, self.y)
		elif direction == '2l':
			return Position(self.y, -self.x)
		elif direction == '2r': # (0, -1) -> (1,0) -> (0,1) -> (-1,0)
			return Position(-self.y, self.x)
		else:
			return self
	


	@staticmethod
	def random(min, max):
		x = random.randint(min.x, max.x)
		y = random.randint(min.y, max.y)
		return Position(x,y)
	
# --- Class Spell ---
class Spell:
	
	@property
	def Recoils(self): return self.healing < 0
	@property
	def Heals(self): return self.healing > 0
	@property
	def Damaging(self): return self.damage > 0
	@property
	def Healing(self): return self.damage < 0
	
	def __init__(self, _name, _damage, _healing, _manaCost, _range, _directed, _stun=0, _extra=None):
		self.damage = _damage
		self.healing = _healing
		self.stun = _stun
		self.directed = _directed
		self.name = _name
		self.manaCost = _manaCost
		self.range = _range
		self.extra = _extra
	
	
	def Cast(self, player, world): player.CastSpell(self,False)
	def __repr__(self):
		return self.name+str(self.manaCost)


# --- Classes Spells e Extras (Constantes e Funções) ---
class Extras:
	def __init__(self):
		pass
	def normalize(self,number):
		a = 1 if number != 0 else 0
		a = -a if number < 0 else a
		return a
	def normalizeVec(self,vec):
		return Position(self.normalize(vec.x),self.normalize(vec.y))
	def LogCoordinate(self, player,  world,  boolean=False):
		player.Logposition()
		return None
	def LogClosestExit(self,player,world,write=True):
		if not world.stairs:
			if write:
				print("Nenhuma escada encontrada.")
			return None
		
		target = min(
			world.stairs,
			key=lambda s: (s.pos.x - player.x)**2 + (s.pos.y - player.y)**2
		)
		
		
		if target != None and write:
			# Usando adição de strings
			print("Escada encontrada em "+ str(target.pos - player.pos))
		
		return target

	
	def GetClosestEnemyPos(self, player,  world, write=True):

		if not world.enemies:
			if write:
				print("Nenhum inimigo encontrado.")
			return None
	
		target = min(
			world.enemies,
			key=lambda e: (e.x - player.x)**2 + (e.y - player.y)**2
		)
		
		
		if target != None and write:
			# Usando adição de strings
			print("Inimigo encontrado em (" + str(target.x - player.x) + ", " + str(-(target.y - player.y)) + ")")
		
		return target
	
	
	def LogCoordinates(self, player,  world,  boolean=False):
		print("Position: ", end="")
		ex = Extras()
		ex.LogCoordinate( player,  world,  boolean)
		
		e = ex.GetClosestEnemyPos(player,  world,   False)
		if e != None:
			print("Postion of closest enemy: ", end="")
			e.Logposition()
		
		return None
	
	def HealConstructor(self, amount):
		def HealSelf(player, world, boolean=False):
			player.health += amount
			player.health = min(player.health,player.maxHealth)
		return HealSelf
	def ManaRegenConstructor(self, amount):
		def ManaSelf(player, world, boolean=False):
			player.mana += amount
			player.mana = min(player.mana,player.maxMana)
		return ManaSelf
	def CastSpellConstructor(self, spell):		
		def cast(player, world, boolean=False):
			spell.Cast(player,world)
		return cast
	def LearnSpellConstructor(self, spell):
		def learn(player, world, boolean=False):
			player.spells.append(spell) if not spell in player.spells else ...
		return learn
	def ReceiveRandomConstructor(self, loot_pool:list['ItemType']):
		def receive(player, world, boolean=False):
			Itype = random.choice(loot_pool)
			it = Itype.Item(1)
			it.addToPlayer(player)
		return receive
	def DashConstructor(self, distance):
		def dash(player, world, boolean=False):
			dx, dy = player.last_move
			player.Move(dx * distance, dy * distance)
		return dash
	def PushLastMove(self,player,world,boolean=False):
		enemy = [e for e in world.enemies if e.pos == player.pos + player.last_move]
		if enemy:
			dx, dy = player.last_move
			enemy[0].Move(dx, dy, world)
	def PushRadiusConstructor(self,radius):
		extras = Extras()
		def push(self,player,world,boolean=False):
			enemies = [e for e in world.enemies if e.pos.euclidean_distance(player.pos) <= radius and e.pos != player.pos]
			for enemy in enemies:
				if enemy:
					dx, dy = enemy.pos - player.pos
					enemy.Move(extras.normalize(dx), extras.normalize(dy), world)
		
	
	

extras = Extras()
class Spells:
	NoSpell = Spell("None", 0, 0, 0, 0, False)
	Fireball = Spell("Fireball", 5, 0, 3, 4,True)
	Heal = Spell("Heal", 0, 5, 3, 0, False)
	IceSpike = Spell("Ice Spike", 4, 0, 4, 7,True, 4)
	HealAura = Spell("Heal Aura", -3, 3, 4, 5, False)
	Radar = Spell("Radar", 0, 0, 3, 10, False, 0, extras.GetClosestEnemyPos)
	Explosion = Spell("Explosion", 7, 0, 5, 3, False, 2)
	Dash = Spell("Dash", 0, 0, 2, 0, False, 0, extras.DashConstructor(2))
	Force = Spell("Force", 1, 0, 3, 3, False, 2, extras.PushRadiusConstructor(2))


	# ===============================================




# --- Classes ItemType, ItemClass, Item, Drop (Itens) ---
# Simplificada
class ItemType:
	def __init__(self, _name, dict_func, _uses):
		self.name = _name
		self.function = dict_func
		self.uses = _uses
	def Item(self, quantity): 
		return Item(self,quantity)
	def __str__(self):
		return self.name
	def __repr__(self):
		return self.name + str(self.uses) + str(self.function.__name__)
	def __eq__(self,other):
		if type(other) != ItemType:
			return False
		return self.name == other.name and self.function == other.function and self.uses == other.uses

	
class ItemClass:
	def __init__(self,name,constructor_function,uses=1):
		'''
	
		:params:
			:name: The name of the class, must contain spaces.

			:constructor_function: A function that returns a secondary function, which uses 3 arguments: a Player, a World and a Boolean
		
			:uses: How many times you can use the item before having to use another
		'''
		self.name = name
		self.function = constructor_function
		self.uses = uses
	def createItemType(self,prefix,extra,isSufix=False):
		return ItemType((self.name + prefix) if isSufix else (prefix + self.name),self.function(extra),self.uses)	
	def __str__(self):
		return 'Class '+ self.name
	def __repr__(self):
		return self.name + str(self.uses)



class ItemClasses:
	SpellScroll = ItemClass('Spell Scroll',extras.CastSpellConstructor,1)
	HealthPotion = ItemClass('Health Potion',extras.HealConstructor,2)
	ManaPotion = ItemClass('Mana Potion',extras.ManaRegenConstructor,2)
	Crate = ItemClass('Crate',extras.ReceiveRandomConstructor,1)
	Grimoire = ItemClass('Grimoire',extras.LearnSpellConstructor,1)

class Items:
	NoneItemType = ItemType("None", None, None)
	CompassType = ItemType("Compass", extras.LogClosestExit, 1)
	MapType = ItemType("Map", extras.LogCoordinates, None)
	IceScrollType = ItemClasses.SpellScroll.createItemType('Ice Spike ', Spells.IceSpike)
	FireScrollType = ItemClasses.SpellScroll.createItemType('Fireball ', Spells.Fireball)
	ExplosionScrollType = ItemClasses.SpellScroll.createItemType('Explosion ',Spells.Explosion)
	SmallManaPotionType = ItemClasses.ManaPotion.createItemType('Small ',2)
	SmallHealthPotionType = ItemClasses.HealthPotion.createItemType('Small ',2)
	PotionCrateType = ItemClasses.Crate.createItemType('Potion ', [SmallHealthPotionType, SmallManaPotionType])
	DashScrollType = ItemClasses.SpellScroll.createItemType('Dash ', Spells.Dash)
	DashGrimoireType = ItemClasses.Grimoire.createItemType('Dash ', Spells.Dash)
	ForceGrimoireType = ItemClasses.Grimoire.createItemType('Force ', Spells.Force)
	ForceScrollType = ItemClasses.SpellScroll.createItemType('Force ', Spells.Force)
	SpellScrollCrateType = ItemClasses.Crate.createItemType('Spell Scroll ', [IceScrollType, FireScrollType, ExplosionScrollType, DashScrollType, ForceScrollType])
	
class Item:
	def __init__(self, _itemType, _quantity, extra = None):
		self.name = _itemType.name
		self.itemType = _itemType
		self.quantity = _quantity
		self.uses = _itemType.uses
		self.extra = extra
		
	def isIn(self,player:'Player'):
		iTs = []
		for it in player.items:
			list.append(iTs,it.itemType)
		return (self.itemType in iTs)
	def playerInventoryType(self,player) -> list[ItemType]:
		iTs = []
		for it in player.items:
			iTs.append(it.itemType)
		return iTs
	def addToPlayer(self,player):
		iTs: list = self.playerInventoryType(player)
		if self.isIn(player):
			ind = iTs.index(self.itemType)
			item = player.items[ind]
			item.quantity += self.quantity
		else:
			player.items.append(self)


	def utilize(self, player, world):
		if self.itemType.function != None:
			self.itemType.function(player, world)
			
		if self.uses != None:
			self.uses -= 1
			if self.uses <= 0:
				self.quantity -= 1
				self.uses = self.itemType.uses
				if self.quantity <= 0:
					player.items.remove(self)
	def __eq__(self,other):
		if type(other) != Item:
			return False
		return self.itemType == other.itemType  and self.quantity == other.quantity

	def __str__(self):
		return str(self.itemType) +': ('+ str(self.quantity) +' , '+ str(self.uses) + ')'
	def __repr__(self):
		return str((self.itemType, self.quantity, self.uses, self.extra != None)) 
class Drop:
	def __init__(self,pos,item_type,quantity):

		self.pos = pos
		self.item:Item = item_type.Item(quantity)
	

	
	def collect(self,player,world):
	
		
		self.item.addToPlayer(player)
		world.RemoveBeing(self)
		print(f'Collected {self.item.quantity} {self.item.name}s')
	def __str__(self):
		return 'Drop:  pos:'+ str(self.pos) + 'Item: ' + str(self.item) 
	def __repr__(self):
		return 'D: '+ str(self.pos) + str(self.item)
	def __eq__(self,other):
		if type(other) != Drop:
			return False
		return self.pos == other.pos and self.item == other.item
# ===============================================
# --- Class Enemy ---

class Enemy:

	def __init__ (self, _health, _attack, _pos):
		self.health = _health
		self.attack = _attack
		self.x = _pos.x
		self.y = _pos.y
		self.stun = 0
	
	@property
	def pos(self):
		return Position(self.x, self.y)
	@pos.setter
	def pos(self, value):
		self.x, self.y = value
	
	def Attack(self, target_pos, world):
		if self.stun <= 0:
			for being in world.beings:
				if isinstance(being, Player) and being.pos == target_pos:
					being.health -= self.attack
					# Adição de strings
					return being
		else:
			self.stun -= 1
			# Adição de strings
			return None
		return None
	
	def isSurrounded(self,world):
		directions = [Position(1,0), Position(-1,0), Position(0,1), Position(0,-1)]
		for direction in directions:
			adjacent_pos = self.pos + direction
			if world.GetSymbolAtposition(adjacent_pos) in '#xk':
				return False
		return True
	def Move(self, delta, world):
		if self.stun <= 0:
			pos = self.pos
			tempX = self.x + delta.x
			tempY = self.y + delta.y
			temp = Position(tempX, tempY)
			blocked = False
			# wall, player, enemy, stairs
			for being in world.colliders:
				if being.pos == temp:
					blocked = True
			
			#out of bounds
			if world.GetSymbolAtposition(temp, ignorePlayers=True) in '#':
				if self.isSurrounded(world):
					blocked = True
				else:
					if world.GetSymbolAtposition(pos.rotate('r')) == '#':
						if world.GetSymbolAtposition(pos.rotate('l')) == '#':
							blocked = True
						else:
							self.Move(delta.rotate('l'), world)
					else:
						self.Move(delta.rotate('r'), world)
				

					
				
			if world.GetSymbolAtposition(Position(tempX, tempY)) == '@':
				self.Attack(Position(tempX, tempY), world)
				blocked = True
			if not blocked:
				self.x = tempX
				self.y = tempY
		else:
			self.stun -= 1

	def distance_to(self, target_pos):
		return abs(self.x - target_pos.x) + abs(self.y - target_pos.y)
	def MoveTowardsTarget(self, target_pos, world):
		if self.stun > 0:
			self.stun -= 1
			return
		x_dist = self.x - target_pos.x
		y_dist = self.y - target_pos.y
		if abs(x_dist) > abs(y_dist):
			step_x = -1 if x_dist > 0 else 1
			self.Move(Position(step_x, 0), world)
		else:
			step_y = -1 if y_dist > 0 else 1
			self.Move(Position(0, step_y), world)

	def Logposition(self):
		print(str((self.x,-self.y)))
	def __str__(self):
		return 'Enemy:'+str(self.pos)
	def __repr__(self):
		return 'E: '+str((self.pos,self.attack,self.health,self.stun))


# --- Classe Player (Jogador) ---
class Player:
	def __init__(self, _spells, world):
		self.x = 0
		self.y = 0
		self.last_move = Position(0, 0)
		self.win = False
		self.maxHealth = 50
		self.health = 50
		self.maxMana = 50
		self.mana = 50
		self.spellIndex = 0
		self.itemIndex = 0
		self.money = 0
		self.spells = _spells
		self.items:list[Item] = []
		self.world: World = world
		world.AddBeing(self)
		
	def reset(self):
		self.health = self.maxHealth
		self.mana = self.maxMana
		self.pos = Position(0,0)
	@property
	def pos(self):
		return Position(self.x, self.y)
	@pos.setter
	def pos(self, value):
		self.x, self.y = value
	@property
	def CurrentSpell(self):
		r =  Spells.NoSpell if len(self.spells) == 0 else self.spells[self.spellIndex]
		return r
		
	@property
	def CurrentItem(self):
		try:
			r =  Item(Items.NoneItemType,1) if len(self.items) == 0 else self.items[self.itemIndex]
		except IndexError:
			self.itemIndex -= 1
			r =  Item(Items.NoneItemType,1) if len(self.items) == 0 else self.items[self.itemIndex]
			
			
		return r
	@property
	def IsDead(self):
		return self.health <= 0

	def CheckDeath(self):
		if self.IsDead:
			self.world.RemoveBeing(self)
			print("O jogador morreu!")
		return self.IsDead
	def Move(self, deltaX, deltaY):
		world = self.world
		self.last_move = Position(deltaX, deltaY)
		tempX = self.x + deltaX
		tempY = self.y + deltaY
		blocked = False
		enemy = None
		
		for e in world.enemies:
			if e.pos == Position(tempX, tempY):
				enemy = e
				blocked = True
				break
		for d in world.items:
			d:'Drop'
			if d.pos == Position(tempX, tempY):
				d.collect(self,world)
		for s in world.stairs:
			
			if s.pos == Position(tempX,tempY):
				s.Use(self)
				
		
		if world.GetSymbolAtposition(Position(tempX, tempY), ignorePlayers=True) == '#':
			blocked = True
		
		if not blocked:
			self.x = tempX
			self.y = tempY
		
		if enemy:
			enemy.health -= 1

	def GetCloseEnemies(self, range_val):
		world = self.world
		closeEnemies = []
		for enemy in world.enemies:
			dx = abs(enemy.x - self.x)
			dy = abs(enemy.y - self.y)
			if (dx + dy) <= range_val and (dx != 0 or dy != 0):
				closeEnemies.append(enemy)
		return closeEnemies
	
	def ApplyDamageAndEffects(self, enemy, spell):
		enemy.health -= spell.damage
		enemy.stun += spell.stun
		world = self.world

		if spell.damage != 0:
			# Adição de strings
			msg = f"Enemy at {enemy.pos - self.pos} took {(spell.damage)} damage."
			print(msg)
		else:
			print(f"Enemy at {enemy.pos-self.pos}")


		if spell.stun > 0:
			# Adição de strings
			print(f"Stun: +{str(spell.stun)}")

		if enemy.health <= 0:
			world.RemoveBeing(enemy)
			# Adição de strings
			print(f"-> Enemy at {((enemy.x - self.x,  self.y - enemy.y))} defeated")
		
	
	
	def CastSpell(self, spell = None, useMana=True):
		world = self.world
		if spell == None:
			spell = self.CurrentSpell
		
		if spell.extra != None:
			spell.extra(self, world)
			

		if (self.mana - spell.manaCost < 0):
			# Adição de strings
			print(f"Not enough mana to cast {spell.name} ({self.mana}/{spell.manaCost}).")
			return
		if useMana:
			self.mana -= spell.manaCost

		if (spell.Heals or spell.Recoils):
			self.health += spell.healing
			self.health = min(self.health, self.maxHealth)
			
			# Adição de strings
			if spell.Heals:
				print(f"{spell.name} cast\nHealth: {str(self.health)}\nMana: {str(self.mana)}.")
			elif spell.Recoils:
				print(f"{spell.name} cast\nPlayer hit by recoil!\nHealth: {str(self.health)}")
		

		if (spell.Damaging or spell.Healing) and spell.directed:
			if self.last_move == Position(0, 0):
				print("No direction to shoot at.")
				return
			
			(dx, dy) = self.last_move
			target_hit = False
			for i in range(1, spell.range + 1):
				targetX = self.x + (dx * i)
				targetY = self.y + (dy * i)

				targetEnemy = next((e for e in world.enemies if e.pos == Position(targetX, targetY)), None)

				if targetEnemy != None:
					self.ApplyDamageAndEffects(targetEnemy, spell)
					# Adição de strings
					print(f"{spell.name} was cast in the direction {(dx, dy)} and hit {str((self.x - targetEnemy.x , self.y - targetEnemy.y))}")
					target_hit = True
					break
			
			if not target_hit:
				print(f"{spell.name} was cast in the direction {(dx, dy)} but didn't hit anything")
		
		elif (spell.Damaging or spell.Healing) and not spell.directed:
			targets = self.GetCloseEnemies(spell.range)

			if len(targets) > 0:
				# Adição de strings
				print(spell.name + " lancado! Atingindo " + str(len(targets)) + " inimigos no alcance " + str(spell.range) + "...")
				for enemy in targets:
					self.ApplyDamageAndEffects(enemy, spell)
			else:

				print(spell.name + " lancado, mas nenhum inimigo estava no alcance " + str(spell.range) + ".")

	

	def ChangeSpell(self):
		if len(self.spells) > 1:
			self.spellIndex = (self.spellIndex + 1) % len(self.spells)

			print(f"Spell swapped to {self.CurrentSpell.name}.")
			return self.CurrentSpell
	
	def Logposition(self):
		print(str(self.pos))

	def ChangeItem(self):
		if len(self.items) > 1:
			self.itemIndex = (self.itemIndex + 1) % len(self.items)

			print("Item alterado para " + self.CurrentItem.name + ".")
			return self.CurrentItem
	def UseItem(self):
		world = self.world
		item = self.CurrentItem
		item.utilize(self,world)
	def __str__(self):
		return ('Player: '+ str(self.pos))
	def __repr__(self):
		return ('P: '+str((self.pos, self.health,self.mana,self.CurrentSpell,self.CurrentItem)))
	def ChangeWorld(self,new_world):
		old_world = self.world
		old_world.RemoveBeing(self)
		self.world = new_world
		new_world.AddBeing(self)
		self.reset()
		
# --- Classe World (Mundo) ---
class World:
	

	def __init__(self, size = 50):
		self.beings = []
		self.players = []
		self.enemies = []
		self.stairs = []
		self.walls = []
		self.items = []
		
		self.worldSize = size
	
	@property
	def colliders(self):
		return self.enemies + self.players + self.stairs + self.walls
		
	def DrawWorld(self, drawWidth, drawHeight, player):
		"""Draws the are viewed by the player."""
		
		viewX = player.x - (drawWidth // 2)
		viewY = player.y - (drawHeight // 2)
		
		print("\n" + "=" * (drawWidth * 2))
		for y in range(drawHeight):
			line = ""
			for x in range(drawWidth):
				worldX = viewX + x
				worldY = viewY + y
				currentpos = Position(worldX, worldY)
				
				symbol = self.GetSymbolAtposition(currentpos, ignorePlayers=False)
				line += symbol + " "

			print(line)
		print("=" * (drawWidth * 2))

	def GetSymbolAtposition(self, pos, ignorePlayers = False):
		
		if (not ignorePlayers and 
			any(player.pos == pos for player in self.players)):
			return '@'
		
		enemy = next((e for e in self.enemies if e.pos == pos), None)
		if enemy != None:
			return 'x'
		drop = next((d for d in self.items if d.pos == pos), None)
		if drop != None:
			return '*'
		stair = next((s for s in self.stairs if s.pos == pos), None)
		if stair != None:
			return 'k'
		wall = next((w for w in self.walls if w.pos == pos), None)
		if wall != None:
			return '#'
		posX, posY = pos 
		halfSize = self.worldSize / 2

		if (abs(posX) > halfSize or abs(posY) > halfSize) or (any(wall.pos == pos for wall in self.walls)):
			return '#'
		
		return '_'
	
	def AddBeing(self, being):
		if isinstance(being, Enemy):
			self.enemies.append(being)
		
		if isinstance(being, Player):
			self.players.append(being)
		if isinstance(being,Drop):
			self.items.append(being)
		if type(being).__name__ == 'Stairs':
			self.stairs.append(being)
		if isinstance(being, Position):
			self.walls.append(being)
		self.beings.append(being)
	def RemoveBeing(self, being):
		for collection in [self.enemies, self.players, self.stairs, self.walls, self.items]:
			if being in collection:
				collection.remove(being)
		self.beings.remove(being)
	def SpawnEnemy(self, pos, health=20, attack=5):
		
		for o in self.colliders:
			if o.pos == pos:
				raise ValueError("Posição " + str(pos) + " ja esta ocupada por um ser.")
		
		enemy = Enemy(health, attack, pos)
		self.AddBeing(enemy)
		return enemy
	def SpawnEnemyRandom(self, health=20, attack=5):
		halfSize = self.worldSize // 2
		pos = Position(random.randint(-halfSize, halfSize),
						random.randint(-halfSize, halfSize))
		
		try:
			self.SpawnEnemy(pos, health, attack)
		except ValueError:
			self.SpawnEnemyRandom(health, attack) 
	def SpawnItem(self,pos,type,quantity=1):
		for o in self.stairs + self.players + self.walls:
			if o.pos == pos:
				raise ValueError("posicao " + str(pos) + " ja esta ocupada.")
		
		drop = Drop(pos,type,quantity)
		self.AddBeing(drop)
	def SpawnItemRandom(self, Itype,quantity_pool=[1,1,1,1,1,2,2,2,3]):
		halfSize = self.worldSize // 2
		pos = Position(random.randint(-halfSize, halfSize), 
			   random.randint(-halfSize, halfSize))
		quantity = random.choice(quantity_pool)
		try:
			self.SpawnItem(pos, Itype, quantity)
		except ValueError:
			self.SpawnItemRandom(Itype) 
	def SpawnItemsRandom(self, ItemTypes,quantity_pool=[1,1,1,1,1,2,2,2,3]):
		IType = random.choice(ItemTypes)
		self.SpawnItemRandom(IType,quantity_pool)
	def SpawnStairs(self, pos, leads_to):
		for o in self.beings:
			if o.pos == pos:
				raise ValueError(f"Position {pos} already occupied.")
		
		stairs = Stairs(pos, self, leads_to)
		self.AddBeing(stairs)
		
	def SpawnStairsWorld(self, pos, size, enemy_count=10, loot_pool=[Items.SmallHealthPotionType],item_count=10,rare_loot_pool=[Items.SpellScrollCrateType],rare_item_count=2):
		s = Stairs.createStairWithWorld(pos,self,size,enemy_count, loot_pool,item_count,rare_loot_pool,rare_item_count)
		self.AddBeing(s)
		return s	
	def SpawnStairsRandom(self, loot_pool=[Items.SmallHealthPotionType],rare_loot_pool=[Items.SpellScrollCrateType],hasStairs=False,limit=5,repetitions=0):
		s =  self.SpawnStairsWorld(
			Position.random(Position.xy(-self.worldSize//2), Position.xy(self.worldSize//2)),
			size=random.randint(20,50),
			enemy_count=random.randint(5,15),
			loot_pool=loot_pool,
			item_count=random.randint(5,15),
			rare_loot_pool=rare_loot_pool,
			rare_item_count=random.randint(1,5)
		)
		if hasStairs:
			s.leads_to.SpawnStairsRandom(loot_pool,rare_loot_pool,(repetitions <= limit),limit,repetitions+1)
		return s
	def SpawnWall(self, pos):
		for o in self.colliders:
			if o.pos == pos:
				raise ValueError("Posição " + str(pos) + " ja esta ocupada por um ser.")
		
		wall = pos
	
		self.AddBeing(wall)	
	

	def __str__(self):
		return 'World: Size '+ str(self.worldSize)+' Beings: '+ str(len(self.beings))
	def __repr__(self):
		return 'W: '+ str((self.worldSize,len(self.beings)))
	
class Stairs:
	def __init__(self, pos,from_world, leads_to = None):
		self.pos = pos
		self.from_world = from_world 
		self.leads_to = leads_to if leads_to != None else World(from_world.worldSize)
	def __str__(self):
		return 'Stairs: '+ str(self.pos)+' -> '+ str(self.leads_to)
	def __repr__(self):
		return 'S: '+ str((self.pos,self.leads_to))
	def Use(self, player):
		player.ChangeWorld(self.leads_to)
	@staticmethod
	def createStairWithWorld(pos,curr_world,size,enemy_count=10, loot_pool=[Items.SmallHealthPotionType],item_count=10,rare_loot_pool=[],rare_item_count=2):
		w = World(size)
		for i in range(enemy_count):
			w.SpawnEnemyRandom()
		for i in range(item_count):
			w.SpawnItemsRandom(loot_pool)
		for i in range(rare_item_count):
			w.SpawnItemsRandom(rare_loot_pool,[1])
		return Stairs(pos, curr_world, w)
	
class WinStairs(Stairs):
	def Use(self, player):
		player.win = True

# ===============================================
# === GAME LOOP ===
# ===============================================

class Keys:
	def __init__(self):
		self.a = False
		self.w = False
		self.s = False
		self.d = False
		self.esc = False
		self.e = False
		self.q = False
		self.r = False
		self.f = False
	def check_keys(k):
		user_input = input("Action: ").strip().lower()
		
		k.a = k.w = k.s = k.d = k.e = k.q = k.r = k.esc = k.f = False

		if user_input == 'a': k.a = True
		elif user_input == 'w': k.w = True
		elif user_input == 's': k.s = True
		elif user_input == 'd': k.d = True
		elif user_input == 'e': k.e = True
		elif user_input == 'q': k.q = True
		elif user_input == 'r': k.r = True
		elif user_input == 'f': k.f = True
		elif user_input in ['esc', 'x', 'sair']: k.esc = True

# --- Setup Inicial ---
if __name__ == '__main__':
	print('='*30)
	print(' '*11,'Magi',' '*11)
	print('='*30)

	running = True
	keys = Keys()
	loot_pool = [Items.SmallHealthPotionType, Items.SmallManaPotionType,Items.ExplosionScrollType, Items.DashScrollType]
	rare_loot_pool = [Items.DashGrimoireType,Items.PotionCrateType, Items.ForceGrimoireType,Items.SpellScrollCrateType,Items.CompassType]

	world1 = World(24)
	player = Player(
		[
		Spells.Fireball,
		Spells.IceSpike,
		Spells.Heal
		], world1
	)

	

	
	world2 = world1.SpawnStairsRandom(loot_pool,rare_loot_pool,True)
	for i in range(7):
		world1.SpawnEnemyRandom()
	for i in range(6):
		world1.SpawnItemsRandom(loot_pool)
	for i in range(2):
		world1.SpawnItemsRandom(rare_loot_pool,[1])

	world1.DrawWorld(9, 9, player) 
	

	# --- Game Loop ---
	print("\nCommands: A/S/W/D (Walk), E (Spell), Q (Swap Spell), R (Swap Item), F (Item), X/ESC (Quit)")


	while running:
		
		
		keys.check_keys()
		moved = False
		
		if (keys.esc):
			running = False	
			print("Exiting...")
			break
			
		if keys.a:
			player.Move(-1, 0)
			moved = True
		
		elif (keys.d): 
			player.Move(1, 0)
			moved = True
		
		elif (keys.w):
			player.Move(0, -1)
			moved = True
		
		elif (keys.s):
			player.Move(0, 1)
			moved = True
		
		elif (keys.e):
			player.CastSpell()
		
		elif (keys.q):
			player.ChangeSpell()
		
		elif (keys.r):
			player.ChangeItem()
		elif (keys.f):
			player.UseItem()
		
		else:
			continue
		
		

		if moved or keys.e  or keys.f:
			for enemy in player.world.enemies:
				if enemy.pos.euclidean_distance(player.pos) <= 5:
					enemy.MoveTowardsTarget(player.pos, world1)
		if moved or keys.e  or keys.f or keys.r or keys.q:
			player.world.DrawWorld(9, 9, player) 
		if player.CheckDeath():
			print('You lost...')
			running = False
			break
		if player.win:
			print('You won!')
			running = False
			break
		
		
		
		print("\n")
		print("-" * 35)
		# Adição de strings para a saída de status
		print("HP: " + str(player.health) + " | Mana: " + str(player.mana) + " | Spell: " + player.CurrentSpell.name + " | Item: " + str(player.CurrentItem))
		print("-" * 35)


'''
--TODO--
Loja ($)



'''
