import React from 'react';

const categories = [
  { id: 'dns', label: 'DNS', icon: '🌐' },
  { id: 'vpn', label: 'VPN', icon: '🔒' },
  { id: 'firewall', label: 'Firewall', icon: '🛡️' },
  { id: 'proxy', label: 'Proxy', icon: '🔄' },
];

const CategorySelector = ({ selectedCategory, onSelectCategory }) => {
  return (
    <div className="d-flex flex-wrap gap-2 justify-content-center p-3">
      {categories.map((category) => (
        <button
          key={category.id}
          onClick={() => onSelectCategory(category.id)}
          className={`
            btn btn-lg d-flex align-items-center gap-2 px-4 w-100 border-0 shadow-sm transition
            ${
              selectedCategory === category.id
                ? 'btn-primary'
                : 'btn-light text-dark bg-white hover-shadow'
            }
          `}
          style={{ borderRadius: '50px' }}
        >
          <span className="fs-4">{category.icon}</span>
          {category.label}
        </button>
      ))}
    </div>
  );
};

export default CategorySelector;
