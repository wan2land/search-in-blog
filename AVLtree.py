# -*- coding:utf-8 -*-
#AVL Tree
"""
height(), balence() 는 height 로 변수로 사용할 수 있도록 처리해야합니다.
delete()가 구현되어있지 않음.

"""
class AVLTreeNode :

	def __init__(self, value) :		

		self.value = value

		self.child_left = None
		self.child_right = None

	def __repr__(self) :
		return '<AVLTreeNode : ' + str(self.value) + '>'

	def height(self) :

		if self.child_left is None :
			height_left = 0
		else :
			height_left = self.child_left.height() + 1

		if self.child_right is None :
			height_right = 0
		else :
			height_right = self.child_right.height() + 1

		return max( height_left, height_right )

	def balence(self) :
		if self.child_left is None :
			height_left = 0
		else :
			height_left = self.child_left.height() + 1

		if self.child_right is None :
			height_right = 0
		else :
			height_right = self.child_right.height() + 1

		return height_left - height_right


class AVLTree :

	def __init__(self, *args) :
		
		self.root = None
		
		if len(args) != 0 :
			for arg in args :
				self.insert( arg )

	def __repr__(self) :
		ret = '[Root : ' + str(self.root) + ']\n'
		ret += self._traverse(self.root)

		return ret

	def search( self, key ) :
		return key

	def insert( self, value ) :

		new_node = AVLTreeNode( value )
		
		if self.root is None :
			self.root = new_node
			return True

		stack = []
		#삽입
		pNode = self.root
		while pNode is not None :
			stack.append(pNode)
			if pNode.value == value :
				return True
			elif pNode.value > value :
				if pNode.child_left is None :
					pNode.child_left = new_node
					break
				pNode = pNode.child_left
			elif pNode.value < value :
				if pNode.child_right is None :
					pNode.child_right = new_node
					break
				pNode = pNode.child_right
		#균형맞추기
		self._balence( stack )

		return True

	def _traverse( self, node, tabindex = 0 ) :
		ret = ''
		
		if node is None :
			return ret

		if node.child_left is not None :
			ret += '  ' * (tabindex + 1) + '[Left : ' + str(node.child_left) + ']\n'
			ret += self._traverse(node.child_left, tabindex+1)
		if node.child_right is not None :
			ret += '  ' * (tabindex + 1) + '[Right : ' + str(node.child_right) + ']\n'
			ret += self._traverse(node.child_right, tabindex+1)

		return ret

	def delete( self, value ) :
		pass

	def _balence( self, stack ) :
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
					pNewNode = self._rotateLL(pNode)
				else :
					pNewNode = self._rotateLR(pNode)
			elif balence < -1 :
				child_balence = pNode.child_right.balence()
				if child_balence < 0 :
					pNewNode = self._rotateRR(pNode)
				else :
					pNewNode = self._rotateRL(pNode)

			# 바뀐거 체크.
			if len(stack) == 0 : # Root Node가 변했다는 뜻!! -_-!!
				self.root = pNewNode
			else :
				pParentNode = stack[ len(stack) - 1 ]
				if pParentNode.child_left == pNode :
					pParentNode.child_left = pNewNode
				else :
					pParentNode.child_right = pNewNode

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
		node.child_left = self._rotateRR( node.child_left )
		return self._rotateLL( node )

	def _rotateRL( self, node ) :
		node.child_right = self._rotateLL( node.child_right )
		return self._rotateRR( node )

if __name__ == "__main__" :
	import random
	x = AVLTree()
	for i in range(0,10) :
		x.insert( random.randint(0, 10000000) )
	
	print x	

