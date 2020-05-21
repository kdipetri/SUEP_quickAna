#decay=generic
#decay=darkPho
decay=darkPhoHad

eosls /store/user/kdipetri/SUEP/Production_v0.0/2018/MINIAOD/*mMed-125_mDark-2_temp-2_decay-${decay}_* | sort > mMed-125_mDark-2_temp-2_decay-${decay}.txt 
eosls /store/user/kdipetri/SUEP/Production_v0.0/2018/MINIAOD/*mMed-400_mDark-2_temp-2_decay-${decay}_* | sort > mMed-400_mDark-2_temp-2_decay-${decay}.txt 
eosls /store/user/kdipetri/SUEP/Production_v0.0/2018/MINIAOD/*mMed-750_mDark-2_temp-2_decay-${decay}_* | sort > mMed-750_mDark-2_temp-2_decay-${decay}.txt 
eosls /store/user/kdipetri/SUEP/Production_v0.0/2018/MINIAOD/*mMed-1000_mDark-2_temp-2_decay-${decay}_* | sort > mMed-1000_mDark-2_temp-2_decay-${decay}.txt 
