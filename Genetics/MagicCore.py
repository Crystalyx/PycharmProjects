def construct_light_spell(spell):
    word = ''
    if spell[0] == 1:
        word = word + 'system.call.'
        if spell[1] == 0:
            word = word + 'magic.'
            if spell[2] == 0:
                word = word + 'refill.'
            else:
                word = word + 'mutate.hue.'
        else:
            word = word + 'area.'
            if spell[2] == 0:
                word = word + 'refill.'
            else:
                if spell[3] == 0:
                    if spell[4] == 0:
                        if spell[5] == 0:
                            word = word + 'eat.'
    else:
        word = word + 'trace.on.'
        if spell[1] == 0:
            word = word + 'mutate.'
            if spell[2] != 0:
                word = word + 'mind.'
    return word


def construct_dark_spell(spell):
    word = ''
    if spell[0] == 1:
        word = word + 'system.call.'
        if spell[1] != 0:
            word = word + 'area.'
            if spell[2] != 0:
                if spell[3] == 0:
                    if spell[4] == 0:
                        if spell[5] == 0:
                            word = word + 'eat.'
    else:
        word = word + 'trace.on.'
        if spell[1] == 0:
            word = word + 'mutate.'
            if spell[2] == 0:
                word = word + 'genome.'
        else:
            word = word + 'create.' + 'mind.'
    return word


def refill(game_map, cx, cy, param, hue):
    if game_map[cx][cy][hue] < param:
        game_map[cx][cy][hue] = param
        return game_map[cx][cy][hue]


def cast_light_spell(snak, spell, game_map, count, cx, cy):
    if spell == 'system.call.magic.refill.':
        snak.food = snak.food + 30
        # print('cast spell: ', word)

    if spell == 'system.call.area.refill.':
        snak.food = snak.food - 170
        refill(game_map, cx % count, cy % count, 100, snak.hue)
        refill(game_map, (cx + 1) % count, cy % count, 200, snak.hue)
        refill(game_map, (cx - 1) % count, cy % count, 200, snak.hue)
        refill(game_map, cx % count, (cy + 1) % count, 200, snak.hue)
        refill(game_map, cx % count, (cy - 1) % count, 200, snak.hue)

        refill(game_map, (cx + 1) % count, (cy + 1) % count, 200, snak.hue)
        refill(game_map, (cx - 1) % count, (cy + 1) % count, 200, snak.hue)
        refill(game_map, (cx + 1) % count, (cy - 1) % count, 200, snak.hue)
        refill(game_map, (cx - 1) % count, (cy - 1) % count, 200, snak.hue)

        refill(game_map, (cx + 2) % count, cy % count, 200, snak.hue)
        refill(game_map, (cx - 2) % count, cy % count, 200, snak.hue)
        refill(game_map, cx % count, (cy + 2) % count, 200, snak.hue)
        refill(game_map, cx % count, (cy - 2) % count, 200, snak.hue)
        snak.dead = True
        # print('cast spell: ', word)

    if spell == 'trace.on.mutate.mind.':
        snak.mutate_mind()
        # print('cast spell: ', word)

    if spell == 'system.call.magic.mutate.hue.':
        snak.hue = (snak.hue + 1) % 3
        # print('cast spell: ', word)


def cast_dark_spell(snak, spell, game_map, count, cx, cy):
    if spell == 'system.call.area.eat.':
        snak.food = snak.food + game_map[cx % count][cy % count][snak.hue]
        snak.food = snak.food + game_map[(cx + 1) % count][cy % count][snak.hue]
        snak.food = snak.food + game_map[(cx - 1) % count][cy % count][snak.hue]
        snak.food = snak.food + game_map[cx % count][(cy + 1) % count][snak.hue]
        snak.food = snak.food + game_map[cx % count][(cy - 1) % count][snak.hue]
        game_map[cx % count][cy % count][snak.hue] = 0
        game_map[(cx + 1) % count][cy % count][snak.hue] = 0
        game_map[(cx - 1) % count][cy % count][snak.hue] = 0
        game_map[cx % count][(cy + 1) % count][snak.hue] = 0
        game_map[cx % count][(cy - 1) % count][snak.hue] = 0
        # print('Emergency! cast spell: ', word)
    if spell == 'trace.on.create.mind.':
        snak.pregnant = True
        # print('cast spell: ', word)
    if spell == 'trace.on.mutate.genome.':
        snak.mutate_genome()
        # print('cast spell: ', word)
