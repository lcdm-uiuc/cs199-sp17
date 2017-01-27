#CS199: Applied Cloud Computing


##Common Errors
* If you reboot your VM, you WILL NEED TO REMOUNT THE SHARED FOLDER

`sudo mount -t vboxsf -o rw,uid=1000,gid=1000 NAMEOFYOURSHAREDFOLDERONHOST NAMEOFFOLDERONVMTOSHARETO`

* SSH
`ssh user@localhost -p 2222`
