sense:
	@echo "Copying mirador to /opt"
	@ sudo cp -r . /opt/mirador
	@echo "Copying mirador.service to /usr/lib/systemd/system"
	@ sudo cp mirador.service /usr/lib/systemd/system
	python3 watch.py -c watch.conf -map
	@ sudo systemctl start mirador.service
	@ sudo systemctl daemon-reload


clean:
	@echo "Cleaning..."
	@ sudo rm -rf /opt/mirador
	@ sudo rm -rf /tmp/mirador
	
.PHONY: clean sense