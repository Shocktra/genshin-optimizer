import { afterEach, describe, expect, it, vi } from 'vitest';
import { fetchPlayer, isValidUid, parseStats } from './enka';

afterEach(() => vi.unstubAllGlobals());

const respond = (status, body = {}) => ({ ok: status >= 200 && status < 300, status, json: async () => body });

describe('isValidUid', () => {
  it.each(['700000000', '1800000000'])('accepts %s', (uid) => expect(isValidUid(uid)).toBe(true));
  it.each(['', '123', '70000000a', '7000 00000', '12345678901'])('rejects %p', (uid) =>
    expect(isValidUid(uid)).toBe(false)
  );
});

describe('parseStats', () => {
  it('maps prop ids and converts rates to percent', () => {
    const stats = parseStats({ 2000: 30000, 2001: 1800, 20: 0.65, 22: 1.5, 23: 1.2, 28: 90, 999: 5 });
    expect(stats.hp).toBe(30000);
    expect(stats.atk).toBe(1800);
    expect(stats.critRate).toBeCloseTo(65);
    expect(stats.critDamage).toBeCloseTo(150);
    expect(stats.energyRecharge).toBeCloseTo(120);
    expect(stats.elementalMastery).toBe(90);
    expect(stats).not.toHaveProperty('999');
  });

  it('ignores non-numeric values and missing input', () => {
    expect(parseStats({ 2000: 'x' })).toEqual({});
    expect(parseStats()).toEqual({});
  });
});

describe('fetchPlayer', () => {
  it('rejects an invalid UID without calling the network', async () => {
    const fetchMock = vi.fn();
    vi.stubGlobal('fetch', fetchMock);
    await expect(fetchPlayer('abc')).rejects.toThrow('9 veya 10 haneli');
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it('trims the UID and returns data', async () => {
    const body = { avatarInfoList: [{ avatarId: 1 }] };
    const fetchMock = vi.fn().mockResolvedValue(respond(200, body));
    vi.stubGlobal('fetch', fetchMock);
    await expect(fetchPlayer(' 700000000 ')).resolves.toEqual(body);
    expect(fetchMock.mock.calls[0][0]).toBe('/api/enka/api/uid/700000000');
  });

  it.each([
    [404, 'bulunamadı'],
    [424, 'bakımda'],
    [429, 'Çok fazla istek'],
    [418, 'HTTP 418'],
  ])('maps HTTP %i to a helpful message', async (status, text) => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(respond(status)));
    await expect(fetchPlayer('700000000')).rejects.toThrow(text);
  });

  it('reports an empty showcase', async () => {
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(respond(200, { avatarInfoList: [] })));
    await expect(fetchPlayer('700000000')).rejects.toThrow('Vitrini');
  });
});
