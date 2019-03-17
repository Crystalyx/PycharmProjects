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


def cast_light_spell(snak, spell, world, count, cx, cy):
    if spell == 'system.call.magic.refill.':
        snak.food = snak.food + 30
        # print('cast spell: ', word)

    if spell == 'system.call.area.refill.':
        snak.food = snak.food - 170
        world.refill(cx, cy, 200, snak.hue)
        world.refill(cx + 1, cy, 200, snak.hue)
        world.refill(cx - 1, cy, 200, snak.hue)
        world.refill(cx, cy + 1, 200, snak.hue)

        world.refill(cx, cy - 1, 200, snak.hue)

        world.refill(cx + 1, cy + 1, 200, snak.hue)
        world.refill(cx - 1, cy + 1, 200, snak.hue)
        world.refill(cx + 1, cy - 1, 200, snak.hue)
        world.refill(cx - 1, cy - 1, 200, snak.hue)

        world.refill(cx + 2, cy, 200, snak.hue)
        world.refill(cx - 2, cy, 200, snak.hue)
        world.refill(cx, cy + 2, 200, snak.hue)
        world.refill(cx, cy - 2, 200, snak.hue)
        snak.dead = True
        # print('cast spell: ', word)

    if spell == 'trace.on.mutate.mind.':
        snak.mutate_mind()
        # print('cast spell: ', word)

    if spell == 'system.call.magic.mutate.hue.':
        snak.hue = (snak.hue + 1) % 3
        # print('cast spell: ', word)


def cast_dark_spell(snak, spell, world, count, cx, cy):
    if spell == 'system.call.area.eat.':
        snak.food = snak.food + world.get_food_at_chunk_by_hue(cx, cy, snak.hue)
        snak.food = snak.food + world.get_food_at_chunk_by_hue(cx + 1, cy, snak.hue)
        snak.food = snak.food + world.get_food_at_chunk_by_hue(cx, cy + 1, snak.hue)
        snak.food = snak.food + world.get_food_at_chunk_by_hue(cx - 1, cy, snak.hue)
        snak.food = snak.food + world.get_food_at_chunk_by_hue(cx, cy - 1, snak.hue)
        world.set_food_at_chunk_by_hue(cx, cy, 0, snak.hue)
        world.set_food_at_chunk_by_hue(cx + 1, cy, 0, snak.hue)
        world.set_food_at_chunk_by_hue(cx, cy + 1, 0, snak.hue)
        world.set_food_at_chunk_by_hue(cx - 1, cy, 0, snak.hue)
        world.set_food_at_chunk_by_hue(cx, cy - 1, 0, snak.hue)
        # print('Emergency! cast spell: ', word)
    if spell == 'trace.on.create.mind.':
        snak.pregnant = True
        # print('cast spell: ', word)
    if spell == 'trace.on.mutate.genome.':
        snak.mutate_genome()
        # print('cast spell: ', word)
