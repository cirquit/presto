PROJECT=pbr
INTRO=commonvoice_demo.py 

all: 
	python ${INTRO}

clean:
	rm -rf commonvoice-split* imagenet-split* librispeech-split* owt-split* cream-split* type-split*

