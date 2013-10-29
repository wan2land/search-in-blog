# -*- coding:utf-8 -*-
import SnbLibrary
import shapely



class Rect :
	def __init__(self, min_x, min_y, max_x = None, max_y = None) :
		
		if max_x is None :
			max_x = min_x + 3
		if max_y is None :
			max_y = min_y + 3

		if min_x > max_x :
			min_x, max_x = max_x, min_x
		if min_y > max_y :
			min_y, max_y = max_y, min_y

		self.min_x = min_x
		self.min_y = min_y
		self.max_x = max_x
		self.max_y = max_y

	def __repr__(self) :
		return '<Rect : ' + \
				str(self.min_x) + ',' + \
				str(self.min_y) + ',' + \
				str(self.max_x) + ',' + \
				str(self.max_y) + '>'

	def coords(self) :
		return self.min_x, self.min_y, self.max_x, self.max_y

	def area(self) :
		return abs( (self.max_x - self.min_x) * (self.max_y - self.min_y) )

	"""
	@param target:Rect
	@return Rect
	"""
	def union(self, target) :
		#나중에 Exception으로 바꿔야함.
		if not isinstance(target, Rect) :
			return None

		return Rect(
			min(self.min_x, target.min_x),
			min(self.min_y, target.min_y),
			max(self.max_x, target.max_x),
			max(self.max_y, target.max_y)
		)

def multiRectArea(rect1, rect2) :
	return abs( ( max(rect1.max_x, rect2.max_x) - min(rect1.min_x, rect2.min_x) ) * \
			( max(rect1.max_y, rect2.max_y) - min(rect1.min_y, rect2.min_y) ) )



class RTreeNode :
	def __init__(self, mbb) :

		if not isinstance(mbb, Rect) :
			print 'Error!!'
			return

		self.mbb = mbb

		self.parent = None
		self.child_left = None
		self.child_right = None

	def __repr__(self) :
		return '<RTreeNode : ' + \
				str(self.mbb.min_x) + ',' + \
				str(self.mbb.min_y) + ',' + \
				str(self.mbb.max_x) + ',' + \
				str(self.mbb.max_y) + '>'

	def height(self) :

		if self.child_left is None or isinstance(self.child_left, RTreeLeaf) :
			height_left = 0
		else :
			height_left = self.child_left.height() + 1

		if self.child_right is None or isinstance(self.child_right, RTreeLeaf) :
			height_right = 0
		else :
			height_right = self.child_right.height() + 1

		return max( height_left, height_right )

	def balence(self) :
		if self.child_left is None or isinstance(self.child_left, RTreeLeaf) :
			height_left = 0
		else :
			height_left = self.child_left.height() + 1

		if self.child_right is None or isinstance(self.child_right, RTreeLeaf) :
			height_right = 0
		else :
			height_right = self.child_right.height() + 1

		return height_left - height_right


class RTreeLeaf(RTreeNode) :

	def __init__(self, shape, value = None) :

		# shape -> mbb 변환.
		mbb = shape

		RTreeNode.__init__(self, mbb)

		self.shape = shape
		self.value = value

	def __repr__(self) :
		return '<RTreeLeaf : ' + \
				str(self.mbb.min_x) + ',' + \
				str(self.mbb.min_y) + ',' + \
				str(self.mbb.max_x) + ',' + \
				str(self.mbb.max_y) + '>'


class RTree :

	def __init__(self, *args) :
		
		self.root = None


	def __repr__(self) :
		ret = ''
		for node, depth in self.traversing() :
			ret += '  ' * depth
			ret += '[' + str(node) + ']\n'

		return ret


	def traversing( self, node = None, depth = 0 ) :
		if node is None :
			
			if self.root is None :
				return

			node = self.root


		yield node, depth

		if node.child_left is not None :
			for nn, nd in self.traversing( node.child_left, depth + 1 ) :
				yield nn, nd

		if node.child_right is not None :
			for nn, nd in self.traversing( node.child_right, depth + 1 ) :
				yield nn, nd


	def insert( self, shape, value = None ) :
		leaf_inserted = RTreeLeaf( shape, value )
		
		if self.root is None :
			self.root = leaf_inserted
			return True

		stack = []
		#삽입
		pNode = self.root
		while True :
			stack.append(pNode)

			if isinstance(pNode, RTreeLeaf) :
				self._addLeaf(stack, leaf_inserted)
				break

			#발생하면 안됌.. 제대로 만들었다면.
			if pNode.child_left is None or pNode.child_right is None :
				print '???'
				return

			rect_with_left = multiRectArea( pNode.child_left.mbb, leaf_inserted.mbb )
			rect_with_right = multiRectArea( pNode.child_right.mbb, leaf_inserted.mbb )

			pNode.mbb = pNode.mbb.union( leaf_inserted.mbb )

			if rect_with_left <= rect_with_right :
				pNode = pNode.child_left
			else :
				pNode = pNode.child_right

		self._balence( stack )
		
		return True


	def _addLeaf(self, stack, leaf_inserted) :
		origin_leaf = stack[-1]

		parent_node = origin_leaf.parent
		
		new_node = RTreeNode( origin_leaf.mbb.union( leaf_inserted.mbb ) )
		new_node.child_left = origin_leaf
		new_node.child_right = leaf_inserted
		origin_leaf.parent = new_node
		leaf_inserted.parent = new_node
		
		if parent_node is None : #parent_node 가 없으면 root.
			self.root = new_node
		else :
			if parent_node.child_left == origin_leaf :
				parent_node.child_left = new_node
			elif parent_node.child_right == origin_leaf :
				parent_node.child_right = new_node
			else :
				print '??'

	def _balence(self, stack) :
		# height 재계산 (지금은 필요없음.. height() 라서.)
		while len(stack) != 0 :
			pNode = stack.pop()
			
			if pNode is None :
				print "Warning.. Node is None.. why?"
				continue
			
			balence = pNode.balence()
			if balence >= -1 and balence <= 1 :
				continue
			
			if balence > 1 :
				child_balence = pNode.child_left.balence()
				if child_balence > 0 :
					print stack
					print "LL"
					#pNewNode = self._rotateLL(pNode)
				else :
					print "LR"
					#pNewNode = self._rotateLR(pNode)
			elif balence < -1 :
				pass
				child_balence = pNode.child_right.balence()
				if child_balence < 0 :
					print stack
					print "RR"
					#pNewNode = self._rotateRR(pNode)
				else :
					print stack
					print "RL"
					#pNewNode = self._rotateRL(pNode)

			# 바뀐거 체크.
			"""
			if len(stack) == 0 : # Root Node가 변했다는 뜻!! -_-!!
				self.root = pNewNode
			else :
				pParentNode = stack[- 1]
				if pParentNode.child_left == pNode :
					pParentNode.child_left = pNewNode
				else :
					pParentNode.child_right = pNewNode
			"""
	def _rotateLL( self, node ) :
		newNode = node.child_left
		node.child_left = newNode.child_right
		newNode.child_right = node
		return newNode

	def _rotateRR( self, node ) :
		newNode = node.child_right
		node.child_right = newNode.child_left
		newNode.child_left = node
		return newNode

	def _rotateLR( self, node ) :
		leaf0 = node.child_left.child_left
		leaf1 = node.child_left.child_right.child_left
		leaf2 = node.child_left.child_right.child_right
		leaf3 = node.child_right

		area0 = multiRectArea( leaf0.mbb, leaf1.mbb ) + multiRectArea( leaf2.mbb, leaf3.mbb )
		area1 = multiRectArea( leaf0.mbb, leaf2.mbb ) + multiRectArea( leaf1.mbb, leaf3.mbb )
		area2 = multiRectArea( leaf0.mbb, leaf3.mbb ) + multiRectArea( leaf1.mbb, leaf2.mbb )

		print area0
		print area1
		print area2

		print leaf0
		print leaf1
		print leaf2
		print leaf3
		return
		node.child_left = self._rotateRR( node.child_left )
		return self._rotateLL( node )

	def _rotateRL( self, node ) :
		node.child_right = self._rotateLL( node.child_right )
		return self._rotateRR( node )


if __name__ == "__main__" :
	from Tkinter import Tk, Canvas
	import time

	t = Tk()
	t.title("RTree Test")

	canvas = Canvas(t, width=800, height=600)
	canvas.pack()

	my_rtree = RTree()

	start_point = None

	def drawAll(rtree) :
		canvas.delete("all")
		for node, depth in rtree.traversing() :
			if depth == 0 :
				canvas.create_rectangle( node.mbb.coords(), outline = 'blue', dash = (2,2))
			else :
				if isinstance(node, RTreeLeaf) :
					canvas.create_rectangle( node.mbb.coords() )
				else :
					canvas.create_rectangle( node.mbb.coords(), outline = 'red', dash = (1,3))

	def mousedown(e) :
		global start_point
		start_point = (e.x, e.y)
	
	def mouseup(e) :
		global start_point, my_rtree
		if start_point is not None :

			start  = int(round(time.time() * 1000))

			my_rtree.insert( Rect(start_point[0], start_point[1], e.x, e.y) )
			print my_rtree
			drawAll(my_rtree)
			print 'running time : ' + str( float( int(round(time.time() * 1000)) - start ) / 1000 )
			start = None

	canvas.bind("<ButtonPress-1>", mousedown)
	canvas.bind("<ButtonRelease-1>", mouseup)

	"""
	my_rtree.insert( Rect(40,30) )

	my_rtree.insert( Rect(100,100) )
	my_rtree.insert( Rect(50,88) )

	my_rtree.insert( Rect(60,147) )
	my_rtree.insert( Rect(15,10) )
	my_rtree.insert( Rect(30,55) )

	my_rtree.insert( Rect(39,15) )
	my_rtree.insert( Rect(27,35) )
	my_rtree.insert( Rect(40,65) )
	my_rtree.insert( Rect(15,75) )
	my_rtree.insert( Rect(44,35) )
	"""


	t.mainloop()

	