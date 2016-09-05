clean-pyc:
	find ./ -name "*.pyc" -exec rm -rfv {} ';'
clean:
	rm -rfv build develop-eggs diglets.egg-info dist eggs parts bin
