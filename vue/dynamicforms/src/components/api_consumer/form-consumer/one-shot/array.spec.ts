import FormConsumerOneShotArray from './array';
import ux_def from './array.spec.json';

const mockFn = vi.hoisted(() => vi.fn());

vi.mock('./base', () => ({ default: mockFn }));

describe('Array One Shot', () => {
  it('Create', async () => {
    await FormConsumerOneShotArray({ definition: ux_def, data: [] });

    expect(mockFn.mock.calls.length).toBe(1);
  });
});
