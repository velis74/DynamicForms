import { describe, it, expect } from 'vitest';

import getObjectFromPath from '@/components/util/get-object-from-path';

describe('Get Object From Path', () => {
  it('Parse Object', () => {
    console.log(getObjectFromPath('some.path.somewhere'));
  });
});
