## Drowsy driver detection and alert system

### Installation
1. Create conda environment

```sh
conda create --name drowsiness_env python=3.5
conda activate drowsiness_env
```

2. Install dependencies

```sh
pip install -r requirements.txt
```

3. Run the demo
```sh
python detect_drowsiness.py
```

(or)

4. Run using Docker

```sh
docker-compose up
```

**Note:** To rebuild the container

```sh
docker-compose up --build
```
