import streamlit as st
import pint

def main():
	u = pint.UnitRegistry()
	st.subheader('Unit Converter')
	def converter(f, t):
		return f.to(t).magnitude


	f = u(st.text_input('From').lower())
	t = u(st.text_input('To').lower())

	if t and f:
		if t.magnitude != 1:
			st.error(f'"To" cannot have magnitude')

		elif f.dimensionality != t.dimensionality:
			st.error('Dimensionality mismatch')
		else:
			c = converter(f, t)
			# full = f'From ({f:P~}) to ({t:P~})\n\n{c}'
			full = f'From ({f:P}) to ({t:P})\n\n{c}'
			# fl = str(full)
			st.markdown(full)