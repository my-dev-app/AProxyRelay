with open('test_targets.txt', 'w') as f:
    for _ in range(500):
        f.write('https://gg.my-dev.app/api/v1/steam/filter/categories/\n')
