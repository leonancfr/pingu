export PS1='\h:\w\$ '
umask 022

export LS_OPTIONS='--color=auto'

alias ls='ls $LS_OPTIONS'
alias ll='ls $LS_OPTIONS -l'
alias l='ls $LS_OPTIONS -lA'
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'
alias ducks='du -cks $(ls -A) | sort -rn | head -n11'
alias python='python3'

export PATH=$PATH:/sbin:/usr/sbin:/opt/gabriel/bin

TMOUT=300