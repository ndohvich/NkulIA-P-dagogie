import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { App } from './App';

describe('App', () => {
  it('affiche le titre de statut du projet', () => {
    render(<App />);
    expect(screen.getByText('Fondations en place')).toBeInTheDocument();
  });
});
