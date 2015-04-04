
INSTALL = /usr/bin/install 
OWNER = ec2-user
GROUP = ec2-user
WWW_SRCS = creds.php \
		   css.css \
		   index.php \
		   searchform.php \
		   search.php \
		   showitem.php
WWW_SRCDIR = www
WWW_INSTDIR = /var/itemdb
SCRIPT_SRCS = dbTest.pl \
			  dbSetup.pl \
			  importLokiXml.pl \
			  itemTest.pl \
			  parseLokiXml.pl
SCRIPT_SRCDIR = scripts
SCRIPT_INSTDIR = /usr/local/bin
PM_SRCS = Bonus.pm \
		  Item.pm
PM_INSTDIR = /usr/local/lib64/perl5/
MYSQLDUMP = /usr/bin/mysqldump
DBBACKUPFILE = itemdb-backup-$(shell date +%Y%m%d-%H%M%S).sql 

.PHONY: www-dirs www-install

www-dirs:
	mkdir -p $(WWW_INSTDIR)
	chown root:root $(WWW_INSTDIR)

$(WWW_SRCS):
	$(INSTALL) -m 0664 -o $(OWNER) -g $(GROUP) $(WWW_SRCDIR)/$@ $(WWW_INSTDIR)/$@

www-install: www-dirs $(WWW_SRCS)

.PHONY: pm-install

$(PM_SRCS):
	$(INSTALL) -m 0664 -o root -g root $(SCRIPT_SRCDIR)/$@ $(PM_INSTDIR)/$@

pm-install: $(PM_SRCS)

.PHONY: script-install

$(SCRIPT_SRCS):
	$(INSTALL) -m 0775 -o $(OWNER) -g $(GROUP) $(SCRIPT_SRCDIR)/$@ $(SCRIPT_INSTDIR)/$@

script-install: $(SCRIPT_SRCS)

config-install:
	$(INSTALL) -m 0664 -o root -g root $(SCRIPT_SRCDIR)/my.conf /etc/itemdb.conf

db-backup:
	$(MYSQLDUMP) --defaults-file=/etc/itemdb.conf --no-create-info itemdb > $(DBBACKUPFILE)
	@echo Wrote DB dump to $(DBBACKUPFILE)

db-setup:
	$(SCRIPT_INSTDIR)/dbSetup.pl

install: www-install pm-install script-install config-install db-backup db-setup
