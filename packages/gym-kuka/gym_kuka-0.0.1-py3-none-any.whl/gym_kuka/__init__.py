from gym.envs.registration import register

register(
    id='kuka-v0',
    entry_point='gym_kuka.envs:kukaEnv',
)
