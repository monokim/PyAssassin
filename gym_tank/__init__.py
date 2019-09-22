from gym.envs.registration import register

register(
    id='Pytank-v0',
    entry_point='gym_tank.envs:TankEnv',
    max_episode_steps=2000,
)
